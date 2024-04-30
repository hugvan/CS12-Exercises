from geometry import Vec2
import pyxel as pxl
from dataclasses import dataclass

@dataclass
class BilliardBall:
    position: Vec2
    velocity: Vec2
    friction: float
    radius: float
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

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 200

class Game:
    def __init__(self) -> None:
        
        self.init_gamestate()
        pxl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="One Billiard")
        pxl.run(self.update, self.draw)

    def init_gamestate(self):
        TABLE_FRICTION = 0.98
        RADIUS = 10.0
        start_pos = Vec2(SCREEN_WIDTH//4, SCREEN_HEIGHT//2)

        cue_ball: BilliardBall = BilliardBall(start_pos, Vec2(), TABLE_FRICTION, RADIUS, pxl.COLOR_WHITE)
        pool_topleft = Vec2(20, 20)
        pool_botright = Vec2(SCREEN_WIDTH, SCREEN_HEIGHT) - pool_topleft

        self.game_state: GameState = GameState(cue_ball, [], pool_topleft, pool_botright, False)
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

        for ball in [self.game_state.cue_ball]:
            ball.position += ball.velocity
            ball.velocity *= ball.friction

            if not (min_bound.y <= ball.top_y <= ball.bot_y <= max_bound.y):
                ball.velocity = ball.velocity.reflect("Y")

            if not (min_bound.x <= ball.left_x <= ball.right_x <= max_bound.x):
                ball.velocity = ball.velocity.reflect("X")

            if stop_simulating and abs(ball.velocity) > EPSILON:
                stop_simulating = False
        
        if stop_simulating:
            self.game_state.simulating = False


    def update(self):
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

        if not game_state.simulating:
            self.draw_stick(self.stick_power)

        #draw cue ball
        pxl.circ(*cue_ball.position.u(), cue_ball.radius, cue_ball.color)

        

Game()