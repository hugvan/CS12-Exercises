import pyxel as pxl
from pyxel import Tilemap
from enum import Enum, IntEnum
from worldtiles import WorldTiles

Point = tuple[int, int]
MoveData = tuple[Point, Point] #Initial, Final
SPRITE_SIZE = 8
LEVEL_SIZE = 16
SCREEN_WIDTH = LEVEL_SIZE * SPRITE_SIZE
SCREEN_HEIGHT = LEVEL_SIZE * SPRITE_SIZE
CARDINALS: dict[str, Point] = {"north": (0,-1),"east": (1,0),"south": (0,1),"west":  (-1,0)}
DIAGONALS: dict[str, tuple[Point, Point]] = {"northeast": (CARDINALS["north"], CARDINALS["east"]),
                                             "northwest": (CARDINALS["north"], CARDINALS["west"]),
                                             "southeast": (CARDINALS["south"], CARDINALS["east"]),
                                             "southwest": (CARDINALS["south"], CARDINALS["west"]),}

class ObjectCoord(Point, Enum):
    NONE = (0,0)
    PLAYER = (0,1)
    BOX = (1,0)
    BUTTON = (1,1)
    FLAG = (2,1)
    WALL = (2,5)

LAYERS = 3
class Layer(IntEnum):
    FLOOR = 0
    GROUND = 1
    BODY = 2

OBJS_LAYERS: dict[Point, int] = {ObjectCoord.PLAYER: Layer.BODY, 
                                 ObjectCoord.BOX: Layer.BODY, 
                                 ObjectCoord.WALL: Layer.BODY, 
                                 ObjectCoord.BUTTON: Layer.GROUND, 
                                 ObjectCoord.FLAG: Layer.GROUND}
IMMOVABLE = {ObjectCoord.WALL}
PUSHABLE = {ObjectCoord.BOX}

def p(coord: Point, offset: Point = (0,0)) -> Point:
    return (coord[0]*SPRITE_SIZE + offset[0], coord[1]*SPRITE_SIZE + offset[1])

def add(a: Point, b: Point) -> Point:
    return (a[0] + b[0], a[1]+ b[1])

def mul(a: Point, s: int) -> Point:
    return (a[0] * s, a[1] * s)


class Sokoban():
    def __init__(self, level_num: int) -> None:
        self.level = level_num
        self.moves: list[list[MoveData]] = []
        self.tiles: WorldTiles = WorldTiles((LEVEL_SIZE, LEVEL_SIZE), 
                                                  LAYERS,
                                                  ObjectCoord.NONE,
                                                  OBJS_LAYERS,
                                                  dict()
                                                  )
        self.player_loc: Point

        pxl.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        pxl.load("SPRITES.pyxres")
        self.init_level(self.level)

        pxl.run(self.update, self.draw)

    def init_level(self, lvl: int) -> None:
        tilemap = pxl.tilemaps[0]
        self.tiles.set_area((0,0), tilemap, (LEVEL_SIZE*lvl,0), (LEVEL_SIZE*(lvl+1),LEVEL_SIZE))
        
        self.player_loc = self.tiles.find_objs(ObjectCoord.PLAYER)[0]
        self.tiles.del_obj(self.player_loc, Layer.BODY) #player should no longer appear in worldtiles

        self.moves: list[list[MoveData]] = []

    def move(self, vector: Point) -> None:
        new_loc = add(self.player_loc, vector)
        
        if self.tiles.get_obj(new_loc, Layer.BODY) in IMMOVABLE:
            self.curr_moveset.append((self.player_loc, self.player_loc))
            return
        elif self.tiles.get_obj(new_loc, Layer.BODY) in PUSHABLE and not self.push(new_loc, vector):
            self.curr_moveset.append((self.player_loc, self.player_loc))
            return
        
        self.curr_moveset.append((self.player_loc, new_loc)) 
        self.player_loc = new_loc 

    def push(self, box_loc: Point, vector: Point) -> bool:
        new_loc = add(box_loc, vector)
        if self.tiles.get_obj(new_loc, Layer.BODY) in IMMOVABLE:
            return False
        elif self.tiles.get_obj(new_loc, Layer.BODY) in PUSHABLE and not self.push(new_loc, vector):
            return False
        
        self.curr_moveset.append((box_loc, new_loc))
        self.tiles.swap_obj(box_loc, new_loc, Layer.BODY)
        return True

    def undo(self):
        if not self.moves:
            return
        
        last_moves = self.moves.pop()
        for initial, final in reversed(last_moves):
            if final == self.player_loc:
                self.player_loc = initial
                continue
            #TODO: This only works for boxes
            self.tiles.swap_obj(initial, final, Layer.BODY)

    def check_interact(self):
        under_player = self.tiles.get_obj(self.player_loc, Layer.GROUND)
        if under_player == ObjectCoord.FLAG:
            self.touch_flag()
        

    def touch_flag(self):
        btns = self.tiles.find_objs(ObjectCoord.BUTTON)
        for btn in btns:
            top = self.tiles.get_obj(btn, Layer.BODY)
            if top == ObjectCoord.NONE:
                return
        self.level += 1
        self.init_level(self.level)
        

    def update(self):
        if pxl.btnp(pxl.KEY_Z, hold=10, repeat=3):
            self.undo()
            return

        self.curr_moveset: list[MoveData] = []

        if pxl.btnp(pxl.KEY_W, hold=10, repeat=3):
            self.move((0,-1))
        if pxl.btnp(pxl.KEY_A, hold=10, repeat=3):
            self.move((-1,0))
        if pxl.btnp(pxl.KEY_S, hold=10, repeat=3):
            self.move((0, 1))
        if pxl.btnp(pxl.KEY_D, hold=10, repeat=3):
            self.move(( 1,0))

        if self.curr_moveset:
            self.moves.append(self.curr_moveset)
        
        self.check_interact()

    def draw_obj(self, coord: Point, type: Point):
        pxl.blt(*p(coord), 0, *p(type), *p((1,1)), 0)

    def draw_wall(self, coord: Point):
        self.draw_obj(coord, ObjectCoord.WALL)
        
        for neighbor in CARDINALS.values():
            n = add(coord, neighbor)
            if self.tiles.get_obj(n, Layer.BODY) != ObjectCoord.WALL:
                furnish = add(ObjectCoord.WALL, neighbor)
                self.draw_obj(coord, furnish)
        
        for nv, nh in DIAGONALS.values():
            diagonal = add(nv, nh)
            n1 = add(coord, nv)
            n2 = add(coord, nh)

            #both are not walls (convex corner)
            if self.tiles.get_obj(n1, Layer.BODY) != ObjectCoord.WALL and self.tiles.get_obj(n2, Layer.BODY) != ObjectCoord.WALL:
                furnish = add(ObjectCoord.WALL, diagonal)
                self.draw_obj(coord, furnish)
            #both are walls (concave corner)
            elif self.tiles.get_obj(n1, Layer.BODY) == ObjectCoord.WALL and self.tiles.get_obj(n2, Layer.BODY) == ObjectCoord.WALL:
                n3 = add(coord, diagonal)
                if self.tiles.get_obj(n3, Layer.BODY) == ObjectCoord.WALL:
                    continue
                furnish = add(ObjectCoord.WALL, mul(diagonal, 2))
                self.draw_obj(coord, furnish)

    def draw(self):
        pxl.cls(0)
        
        for x in range(LEVEL_SIZE):
            for y in range(LEVEL_SIZE):
                ground_obj = self.tiles.get_obj((x,y), Layer.GROUND)
                self.draw_obj((x,y), ground_obj)

                body_obj = self.tiles.get_obj((x,y), Layer.BODY)
                if body_obj == ObjectCoord.WALL:
                    self.draw_wall((x, y))
                    continue
                self.draw_obj((x,y), body_obj)
        
        #draw player
        self.draw_obj(self.player_loc, ObjectCoord.PLAYER)

Sokoban(0)
