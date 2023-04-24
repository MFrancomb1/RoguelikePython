from  __future__ import annotations
from typing import Iterable, TYPE_CHECKING
import numpy as np
from tcod.console import Console

import tile_types

if TYPE_CHECKING:
    from entity import Entity


class GameMap:
    def __init__(self, width: int, height: int, entities: Iterable[Entity] = ()):
        self.width = width
        self.height = height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F") #fill 2d array with wall tiles

        self.visible = np.full((width, height), fill_value=False, order="F")
        self.explored = np.full((width, height), fill_value=False, order="F")

    def in_bounds(self, x, y) -> bool:
        return 0<=x<=self.width and 0<=y<=self.height
    
    def render(self, console) -> None:
        """renders the map if the tile is in the visible array, it uses the light color 
        if the tile is not visible but is explored, it uses the dark color
        otherwise default to "SHROUD"


        Args:
            console (console): game console to print
        """
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible,self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD
        )

        for entity in self.entities:
            if self.visible[entity.x, entity.y]:
                console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)

        