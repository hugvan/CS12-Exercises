import pyxel as pxl
from pyxel import Image
from geometry import Vec2
from functools import cached_property
from dataclasses import dataclass
from math import tan, sin, pi

@dataclass
class RotatableImage:
    """
    Create a reference to a specified area in Image_0, allows for rotated draw calls
    IMPORTANT: Initialize ImageBank, Leave at least 1x1 margin around image
    """
    top_left: Vec2
    bot_right: Vec2
    tr_color: int

    def __post_init__(self):
        self.rotation_canvas = pxl.Image(*self.padded_rect.ui())

    @cached_property
    def width(self) -> float:
        return self.bot_right.x - self.top_left.x
    
    @cached_property
    def height(self) -> float:
        return self.bot_right.y - self.top_left.y

    @cached_property
    def padded_rect(self) -> Vec2:
        max_length = max(self.width, self.height)
        return Vec2(max_length,max_length) * 2

    @cached_property
    def padded_center(self) -> Vec2:
        return self.padded_rect * (0.5)
    
    @cached_property
    def padded_topleft(self) -> Vec2:
        return self.padded_center - Vec2(self.width, self.height) * 0.5

    def rotate_draw(self, angle: float, center_pos: Vec2):
        IMAGE_0 = 0
        #check if at 90 to 270, rotates it 180
        mult = 1
        angle %= 360
        if 90 < angle < 270:
            angle = angle - 180
            mult = -1

        angle *= pi/180

        def shear_x():
            for y in range(int(self.padded_rect.y)):
                sx = (y - self.padded_center.y) * -tan(angle/2) 
                sheared = Vec2(sx, y)
                self.rotation_canvas.blt(*sheared.u(), self.rotation_canvas, 0, y, self.padded_rect.x, 1)
                self.rotation_canvas.rect(0, y, sx, 1, self.tr_color)
                self.rotation_canvas.rect(sx+self.padded_rect.x, y, self.padded_rect.x, 1, self.tr_color)
        
        def shear_y():
            for x in range(int(self.padded_rect.x)):
                sy = (x - self.padded_center.x) * sin(angle)
                sheared = Vec2(x, sy)
                self.rotation_canvas.blt(*sheared.u(), self.rotation_canvas, x, 0, 1, self.padded_rect.y)
                self.rotation_canvas.rect(x, 0, 1, sy, self.tr_color)
                self.rotation_canvas.rect(x, sy+self.padded_rect.y, 1, self.padded_rect.y, self.tr_color)

        #clear image_1 canvas
        self.rotation_canvas.rect(*Vec2().u(), *self.padded_rect.u(), self.tr_color)

        #copy from image_0 to image_1, with padding
        self.rotation_canvas.blt(*self.padded_topleft.u(),
                                IMAGE_0,
                                *self.top_left.u(),
                                self.width * mult,
                                self.height * mult,
                                self.tr_color)

        #shear image_1 by replacing line by line
        shear_x()
        shear_y()
        shear_x()
        
        #DEBUG
        #pxl.blt(*Vec2().u(), 1, *Vec2().u(), 200, 200, pxl.COLOR_BLACK)
        #pxl.rectb(*Vec2().u(), *self.padded_rect.u(), pxl.COLOR_BLACK)
        
        pxl.blt(*(center_pos - self.padded_center).u(), self.rotation_canvas, *Vec2().u(), *self.padded_rect.u(), self.tr_color)



class Game:
    def __init__(self) -> None:
        SCREEN_WIDTH = 200
        SCREEN_HEIGHT = 200
        self.box = RotatableImage(Vec2(0,0),Vec2(15,15), pxl.COLOR_BLACK)
        self.ball = RotatableImage(Vec2(0,48),Vec2(31,79), pxl.COLOR_RED)
        self.big_box = RotatableImage(Vec2(16,0),Vec2(47,47), pxl.COLOR_BLACK)
        
        pxl.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        pxl.load("ROTATIONDATA.pyxres")
        pxl.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pxl.cls(pxl.COLOR_LIME)
        self.big_box.rotate_draw(pxl.frame_count, Vec2(pxl.mouse_x, pxl.mouse_y))
        self.box.rotate_draw(pxl.frame_count * 2.4, Vec2(30,30))
        self.ball.rotate_draw(pxl.frame_count * 10, Vec2(70,70))