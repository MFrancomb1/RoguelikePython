from  __future__ import annotations
from typing import Iterable, Iterator, Optional, TYPE_CHECKING
import numpy as np
from tcod.console import Console

from entity import Actor
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class GameMap:
    def __init__(self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()):
        self.engine = engine
        self.width = width
        self.height = height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F") #fill 2d array with wall tiles

        self.visible = np.full(
            (width, height), fill_value=False, order="F"
        )  # Tiles the player can currently see
        self.explored = np.full(
            (width, height), fill_value=False, order="F"
        )  # Tiles the player has seen before

    @property
    def actors(self) -> Iterator[Actor]:
        """Iterate ove this map's living actors"""
        yield from (
            entity for entity in self.entities if isinstance(entity, Actor) and entity.is_alive
        )

    def in_bounds(self, x, y) -> bool:
        return 0<=x<self.width and 0<=y<self.height
    
    def get_blocking_entity_at_location(self, location_x: int, location_y: int) -> Optional[Entity]:
        for entity in self.entities:
            if ( entity.blocks_movement and entity.x == location_x and entity.y == location_y):
                return entity
        return None
    
    def get_actor_at_location(self, x: int, y:int) -> Optional[Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor
        return None
    
    def render(self, console) -> None:
        """renders the map if the tile is in the visible array, it uses the light color 
        if the tile is not visible but is explored, it uses the dark color
        otherwise default to "SHROUD"


        Args:
            console (console): game console to print
        """
        console.tiles_rgb[0 : self.width, 0 : self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD,
        )

        entities_sorted_for_rendering = sorted(
            self.entities, key=lambda x: x.render_order.value
        )
        
        for entity in entities_sorted_for_rendering:
            if self.visible[entity.x, entity.y]:
                console.print(
                    x=entity.x, y=entity.y, string=entity.char, fg=entity.color
                )

        