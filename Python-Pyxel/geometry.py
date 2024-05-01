from __future__ import annotations
from dataclasses import dataclass
from functools import cached_property

@dataclass(frozen=True)
class Vec2:
    x: float = 0
    y: float = 0

    def u(self) -> tuple[float, float]:
        """Unpack x and y"""
        return (self.x, self.y)

    def __add__(self, other:object) -> Vec2:
        if isinstance(other, Vec2):
            return Vec2(self.x + other.x, self.y + other.y)
        raise ValueError
    
    def __mul__(self, other: object) -> Vec2:
        #scalar multiplication
        if isinstance(other, float|int):
            return Vec2(self.x * other, self.y * other)
        raise ValueError

    def __rmul__(self, other: object) -> Vec2:
        if isinstance(other, float):
            return self * other
        raise ValueError

    def __neg__(self) -> Vec2:
        return self * -1
    
    def __sub__(self, other:object) -> Vec2:
        if isinstance(other, Vec2):
            return self + (-other)
        raise ValueError
    
    @cached_property
    def abs2(self) -> float:
        return (self.x ** 2 + self.y ** 2)

    def __abs__(self) -> float:
        return self.abs2 ** 0.5 

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Vec2):
            return self.x == other.x and self.y == other.y
        return False
    
    def __ne__(self, other: object) -> bool:
        return not (self == other)

    def dot(self, other: object) -> float:
        if isinstance(other, Vec2):
            return (self.x * other.x + self.y * other.y)
        raise ValueError
    
    def cross(self, other: object) -> float:
        if isinstance(other, Vec2):
            return (self.x * other.y - self.y * other.x)
        raise ValueError
    
    def neg_transpose(self, new_x_neg: bool = True) -> Vec2:
        return Vec2(-self.y,self.x) if new_x_neg else Vec2(self.y,-self.x)

    def scale_to(self, magnitude: float = 1) -> Vec2:
        return self * (magnitude / abs(self))
    
    def reflect(self, line: str|Vec2) -> Vec2:
        """line: [y=0], [x=0]"""
        
        match line:
            case "y=0": return Vec2(self.x, -self.y)
            case "x=0": return Vec2(-self.x, self.y)
            case Vec2():
                return 2 * ( self.dot(line) / line.abs2) * line - self
            case _: 
                raise ValueError

