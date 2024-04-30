from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from numpy import uint8
from numpy.typing import NDArray
import pyxel as pxl
from pyxel import Tilemap

Object = tuple[int, int]
Point = tuple[int, int]


class WorldTiles:
    def __init__(self, size: Point, layers: int, empty_obj: Object, objs_layers: dict[Object, int], obj_aliases: dict[Object, list[Object]]) -> None:
        self._arrs: dict[Object, NDArray[uint8]] = {empty_obj: np.zeros(layers, dtype=uint8)}
        self._objs: list[Object] = [empty_obj]

        # turn each object into something like [0, 0, id, 0], to show which layer it is in
        for obj, layer in objs_layers.items():
            id = len(self._objs)
            self._objs.append(obj)
            obj_arr = np.copy(self._arrs[empty_obj])
            obj_arr[layer] = id
            self._arrs[obj] = obj_arr
        
        # turn each alias into something like [id1, id2, id3, 0], for each distinct obj
        # this is because each object is "flat"
        for obj_alias, objs in obj_aliases.items():
            obj_arr = np.copy(self._arrs[empty_obj])
            for obj in objs:
                obj_arr += self._arrs[obj]
            self._arrs[obj_alias] = obj_arr

        self.grid = np.zeros((size[0], size[1], layers), dtype=uint8)

    def get_obj(self, pos: Point, layer: int) -> Object:
        return self._objs[self.grid[pos[0], pos[1], layer]]
    
    def set_obj(self, pos: Point, obj: Object):
        for layer, id in enumerate(self._arrs[obj]):
            if id != 0:
                self.grid[pos[0], pos[1], layer] = id

    def del_obj(self, pos: Point, *layers: int):
        for layer in layers:
            self.grid[pos[0], pos[1], layer] = 0
    
    def swap_obj(self, p1: Point, p2: Point, *layers: int):
        for layer in layers:
            self.grid[p1[0], p1[1], layer], self.grid[p2[0], p2[1], layer] = self.grid[p2[0], p2[1], layer], self.grid[p1[0], p1[1], layer]
    
    def set_area(self, tl: Point, tilemap: Tilemap, tmap_tl: Point, tmap_br: Point):
        for x in range(tmap_tl[0], tmap_br[0]):
            for y in range(tmap_tl[1], tmap_br[1]):
                obj = tilemap.pget(x, y)
                self.grid[tl[0] + x - tmap_tl[0], tl[1] + y -tmap_tl[1]] = self._arrs[obj]

    def find_objs(self, obj: Object) -> list[Point]:
        tile = self._arrs[obj]
        id: int = tile[np.where(tile != 0)][0]

        coords = np.where(self.grid == id)
        ret: list[Point] = []
        for idx in range(np.size(coords, 1)):
            ret.append((coords[0][idx], coords[1][idx]))
        
        return ret
