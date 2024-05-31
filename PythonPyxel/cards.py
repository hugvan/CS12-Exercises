import pyxel as pxl
from rotation_test import RotatableImage
from geometry import Vec2
from dataclasses import dataclass
from random import randint

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 200

@dataclass
class Card(RotatableImage):
    suit: str
    rank: str
    rotation: int = 0

    def rotate_draw(self, center_pos: Vec2):
        return super().rotate_draw(self.rotation, center_pos)

class Game:
    def __init__(self) -> None:
        self.cards: list[Card] = []
        self.cards.append(Card(Vec2(), Vec2(31,47), pxl.COLOR_PURPLE, "spade", "ace", randint(0,360)))

        pxl.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        pxl.load("CARD_DATA.pyxres")
        pxl.run(self.update, self.draw)
    
    def update(self) -> None:
        pass

    def draw(self) -> None:
        pxl.cls(pxl.COLOR_BLACK)

        for card in self.cards:
            card.rotate_draw(Vec2(40, 40))

Game()