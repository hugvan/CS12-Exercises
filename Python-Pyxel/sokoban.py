import pyxel as pxl
from pyxel import Tilemap
from enum import Enum

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
    FLAG = (2,0)
    WALL = (2,5)

GROUNDHEIGHT = {ObjectCoord.FLAG, ObjectCoord.BUTTON}
BODYHEIGHT = {ObjectCoord.WALL, ObjectCoord.BOX}
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
        self.moves: list[list[MoveData]] = []
        
        self.body_tiles: list[list[Point]] = []
        self.ground_tiles: list[list[Point]] = []
        self.player_loc: Point

        pxl.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        pxl.load("SPRITES.pyxres")
        self.init_level(level_num)

        pxl.run(self.update, self.draw)

    def init_level(self, lvl: int) -> None:
        tilemap = pxl.tilemaps[0]
        for x_idx in range(LEVEL_SIZE):
            body_row: list[Point] = []
            ground_row: list[Point] = []
            for y_idx in range(LEVEL_SIZE):
                obj = tilemap.pget(x_idx + lvl * LEVEL_SIZE, y_idx) # type: ignore
                # Player is not in tiles
                if obj == ObjectCoord.PLAYER:
                    self.player_loc = (x_idx, y_idx)
                    body_row.append(ObjectCoord.NONE)
                    ground_row.append(ObjectCoord.NONE)
                    continue
                
                body_row.append(obj if obj in BODYHEIGHT else ObjectCoord.NONE) 
                ground_row.append(obj if obj in GROUNDHEIGHT else ObjectCoord.NONE) 
            self.body_tiles.append(body_row)
            self.ground_tiles.append(ground_row)

    def get_tile(self, coord: Point, height: int) -> Point:
        match height:
            case 0: return self.ground_tiles[coord[0]][coord[1]]
            case 1: return self.body_tiles[coord[0]][coord[1]]
            case _: assert False  

    def set_tile(self, coord: Point, obj: Point, height: int):
        match height:
            case 0: self.ground_tiles[coord[0]][coord[1]] = obj
            case 1: self.body_tiles[coord[0]][coord[1]] = obj
            case _: assert False
        

    def move(self, vector: Point) -> None:
        new_loc = add(self.player_loc, vector)
        
        if self.get_tile(new_loc, 1) in IMMOVABLE:
            self.curr_moveset.append((self.player_loc, self.player_loc))
            return
        elif self.get_tile(new_loc, 1) in PUSHABLE and not self.push(new_loc, vector):
            self.curr_moveset.append((self.player_loc, self.player_loc))
            return
        
        self.curr_moveset.append((self.player_loc, new_loc)) 
        self.player_loc = new_loc 

    def push(self, box_loc: Point, vector: Point) -> bool:
        new_loc = add(box_loc, vector)
        if self.get_tile(new_loc, 1) in IMMOVABLE:
            return False
        elif self.get_tile(new_loc, 1) in PUSHABLE and not self.push(new_loc, vector):
            return False
        
        self.curr_moveset.append((box_loc, new_loc))
        self.set_tile(box_loc, ObjectCoord.NONE, 1)
        self.set_tile(new_loc, ObjectCoord.BOX, 1)
        return True

    def undo(self):
        if not self.moves:
            return
        
        last_moves = self.moves.pop()
        for initial, final in reversed(last_moves):
            if final == self.player_loc:
                self.player_loc = initial
                continue
            self.set_tile(initial, self.get_tile(final, 1), 1)
            self.set_tile(final, ObjectCoord.NONE, 1)

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

    def draw_obj(self, coord: Point, type: Point):
        pxl.blt(*p(coord), 0, *p(type), *p((1,1)), 0)

    def draw_wall(self, coord: Point):
        self.draw_obj(coord, ObjectCoord.WALL)
        
        for neighbor in CARDINALS.values():
            n = add(coord, neighbor)
            if self.get_tile(n, 1) != ObjectCoord.WALL:
                furnish = add(ObjectCoord.WALL, neighbor)
                self.draw_obj(coord, furnish)
        
        for nv, nh in DIAGONALS.values():
            diagonal = add(nv, nh)
            n1 = add(coord, nv)
            n2 = add(coord, nh)

            #both are not walls (convex corner)
            if self.get_tile(n1, 1) != ObjectCoord.WALL and self.get_tile(n2, 1) != ObjectCoord.WALL:
                furnish = add(ObjectCoord.WALL, diagonal)
                self.draw_obj(coord, furnish)
            #both are walls (concave corner)
            elif self.get_tile(n1, 1) == ObjectCoord.WALL and self.get_tile(n2, 1) == ObjectCoord.WALL:
                n3 = add(coord, diagonal)
                if self.get_tile(n3, 1) == ObjectCoord.WALL:
                    continue
                furnish = add(ObjectCoord.WALL, mul(diagonal, 2))
                self.draw_obj(coord, furnish)

    def draw(self):
        pxl.cls(0)
        
        for x in range(LEVEL_SIZE):
            for y in range(LEVEL_SIZE):
                ground_obj = self.get_tile((x,y), 0)
                self.draw_obj((x,y), ground_obj)

                body_obj = self.get_tile((x,y), 1)
                if body_obj == ObjectCoord.WALL:
                    self.draw_wall((x, y))
                    continue
                self.draw_obj((x,y), body_obj)
        
        #draw player
        self.draw_obj(self.player_loc, ObjectCoord.PLAYER)

Sokoban(2)
