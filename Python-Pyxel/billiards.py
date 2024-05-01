from geometry import Vec2
import pyxel as pxl
from pyxel import Tilemap
from dataclasses import dataclass
from functools import cached_property

@dataclass
class BilliardBall:
    position: Vec2
    velocity: Vec2
    friction: float
    radius: float
    mass: float
    color: int #Based on Pyxel

    @property
    def top_y(self) -> float:
        return self.position.y - self.radius
    
    @property
    def bot_y(self) -> float:
        return self.position.y + self.radius
    
    @property
    def left_x(self) -> float:
        return self.position.x - self.radius
    
    @property
    def right_x(self) -> float:
        return self.position.x + self.radius

@dataclass
class GameState:
    cue_ball: BilliardBall
    billiard_balls: list[BilliardBall]
    pool_tl: Vec2
    pool_br: Vec2
    simulating: bool

    @cached_property
    def all_balls(self) -> list[BilliardBall]:
        return [self.cue_ball, *self.billiard_balls]


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 270
BILLIARD_COLORS: list[int] = [pxl.COLOR_YELLOW, pxl.COLOR_DARK_BLUE, pxl.COLOR_RED, pxl.COLOR_PURPLE, 
                              pxl.COLOR_ORANGE, pxl.COLOR_LIME, pxl.COLOR_LIGHT_BLUE, pxl.COLOR_BLACK,]
BILLIARD_ROWS: int = 3
TABLE_FRICTION = 0.98
RADIUS = 10.0
MASS = 10.0
CUE_START: Vec2 = Vec2(SCREEN_WIDTH//4, SCREEN_HEIGHT//2) 

class Game:
    def __init__(self) -> None:
        
        self.init_gamestate()
        pxl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Billiards")
        pxl.run(self.update, self.draw)

    def init_gamestate(self):
        cue_ball: BilliardBall = BilliardBall(CUE_START, Vec2(), TABLE_FRICTION, RADIUS, MASS, pxl.COLOR_WHITE)
        pool_topleft = Vec2(20, 20)
        pool_botright = Vec2(SCREEN_WIDTH, SCREEN_HEIGHT) - pool_topleft

        #automatically make ball starting positions
        ball_starts: list[Vec2] = [CUE_START + Vec2(SCREEN_WIDTH//3,0)]
        for balls_in_col in range(2,BILLIARD_ROWS + 1):
            first_ball = ball_starts[0]
            ball_x = first_ball.x + 2.5*RADIUS*(balls_in_col-1)
            ball_y = first_ball.y - 1.25*RADIUS*(balls_in_col-1)
            for idx in range(balls_in_col):
                ball_starts.append(Vec2(ball_x, ball_y + 2.5*idx*RADIUS))

        billiard_balls: list[BilliardBall] = []
        for num, ball_start in enumerate(ball_starts):
            ball: BilliardBall = BilliardBall(ball_start, Vec2(), TABLE_FRICTION, RADIUS, MASS, BILLIARD_COLORS[num % 8])
            billiard_balls.append(ball)

        #self properties are initialized here
        self.game_state: GameState = GameState(cue_ball, billiard_balls, pool_topleft, pool_botright, False)
        self.stick_power: float = 0.0

    def strike_cue(self):
        game_state = self.game_state
        cue_ball = game_state.cue_ball

        game_state.simulating = True

        mouse_pos = Vec2(pxl.mouse_x, pxl.mouse_y)
        cue_center = self.game_state.cue_ball.position
        c_to_m = (mouse_pos - cue_center).scale_to()
        cue_ball.velocity = c_to_m.scale_to(-self.stick_power)
        
    
    def physics_process(self):
        EPSILON = 10 ** -1
        min_bound = self.game_state.pool_tl
        max_bound = self.game_state.pool_br
        stop_simulating = True

        for idx, ball in enumerate(self.game_state.all_balls):
            ball.position += ball.velocity
            ball.velocity *= ball.friction

            #Wall Collisions
            if not (min_bound.y <= ball.top_y <= ball.bot_y <= max_bound.y):
                ball.position += Vec2(0, min_bound.y - ball.top_y) if ball.top_y < min_bound.y else Vec2(0, max_bound.y - ball.bot_y)
                ball.velocity = ball.velocity.reflect("y=0")

            if not (min_bound.x <= ball.left_x <= ball.right_x <= max_bound.x):
                ball.position += Vec2(min_bound.x - ball.left_x, 0) if ball.left_x < min_bound.x else Vec2(max_bound.x - ball.right_x, 0)
                ball.velocity = ball.velocity.reflect("x=0")

            #Ball Collisions
            for other_ball in self.game_state.all_balls:
                if ball is other_ball:
                    continue
                
                ball_delta = other_ball.position - ball.position
                overlap = other_ball.radius + ball.radius - abs(ball_delta) 
                if overlap >= 0:                 
                    #separate balls before calculating new velocities
                    ball.position -= ball_delta.scale_to(overlap)

                    tangent = ball_delta.neg_transpose()
                    old_bv = ball.velocity
                    ball.velocity = ball.velocity.reflect(tangent) * 0.7
                    other_vx = (ball.mass/other_ball.mass)*(old_bv.x - ball.velocity.x) + other_ball.velocity.x
                    other_vy = (ball.mass/other_ball.mass)*(old_bv.y - ball.velocity.y) + other_ball.velocity.y
                    other_ball.velocity = Vec2(other_vx, other_vy) * 0.7


            #Stop Physics if nothing is moving
            if stop_simulating and abs(ball.velocity) > EPSILON:
                stop_simulating = False
        
        if stop_simulating:
            self.game_state.simulating = False


    def update(self):
        if not self.game_state.simulating:
            if pxl.btn(pxl.MOUSE_BUTTON_LEFT) and self.stick_power < 20:
                self.stick_power += min(1, 1 * (2/ (self.stick_power + 1)))

            if pxl.btnr(pxl.MOUSE_BUTTON_LEFT):
                self.strike_cue()
                self.stick_power = 0
        
        if self.game_state.simulating:
            self.physics_process()
    
    def draw_stick(self, distance: float):
        mouse_pos = Vec2(pxl.mouse_x, pxl.mouse_y)
        cue_center = self.game_state.cue_ball.position

        # A "basis" vector going from cue center to mouse pos 
        c_to_m = (mouse_pos - cue_center).scale_to()
        
        mouse_delta = c_to_m.scale_to(5)
        fixed_mpos = cue_center + c_to_m.scale_to(150 + distance)
        mouse_l = fixed_mpos + mouse_delta.neg_transpose(True)
        mouse_r = fixed_mpos + mouse_delta.neg_transpose(False)

        cue_delta =  (cue_center - mouse_pos).scale_to(2)
        cue_offset = cue_center + c_to_m.scale_to(15 + distance)
        cue_l = cue_offset + cue_delta.neg_transpose(False)
        cue_r = cue_offset + cue_delta.neg_transpose(True)

        pxl.tri(*mouse_l.u(), *mouse_r.u(), *cue_r.u(), pxl.COLOR_BROWN)
        pxl.tri(*cue_l.u(), *cue_r.u(), *mouse_l.u(), pxl.COLOR_BROWN)

    def draw(self):
        pxl.cls(0)
        game_state = self.game_state
        cue_ball = game_state.cue_ball
        
        #draw pool table
        w_and_h = game_state.pool_br - game_state.pool_tl
        pxl.rect(*game_state.pool_tl.u(), *w_and_h.u(), pxl.COLOR_GREEN )

        #draw billiard balls
        for ball in game_state.billiard_balls:
            pxl.circ(*ball.position.u(), ball.radius, ball.color)

        #draw cue ball
        pxl.circ(*cue_ball.position.u(), cue_ball.radius, cue_ball.color)

        if not game_state.simulating:
            self.draw_stick(self.stick_power)

        


Game()