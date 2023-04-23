import numpy as np
from tcod.console import Console

import tile_types

class GameMap:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F") #fill 2d array with wall tiles

        self.visible = np.full((width, height), fill_value=False, order="F")
        self.explored = np.full((width, height), fill_value=False, order="F")

    def in_bounds(self, x, y) -> bool:
        return 0<=x<=self.width and 0<=y<=self.height
    
    def render(self, console) -> None:
        # renders the map
        #if the tile is in the visible array, it uses the light color
        #if the tile is not visible but is explored, it uses the dark color
        #otherwise default to shroud

        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible,self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD
        )