from __future__ import annotations
from typing import Tuple, Iterator, List, TYPE_CHECKING
import tcod
import random

from game_map import GameMap
import tile_types

if TYPE_CHECKING:
    from entity import Entity

class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
    
    @property
    def center(self) -> Tuple[int,int]:
        center_x = int((self.x1+self.x2)/2)
        center_y = int((self.y1+self.y2)/2)
        return center_x,center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)
    
    def intersects(self, other: RectangularRoom) -> bool:
        #returns true if this room overlaps with another room
        return (self.x1<=other.x2 and self.x2 >= other.x1 and self.y1<=other.y2 and self.y2>= other.y1)

    
def tunnel_between(start: Tuple[int,int], end: Tuple[int,int]) -> Iterator[Tuple[int,int]]:
    #return an L shaped tunnel between 2 points
    x1, y1 = start
    x2, y2 = end
    if random.random() <0.5:
        #tunnel horizontally, then vertically
        corner_x, corner_y = x2, y1
    else:
        #tunnel vertically, then horizontally
        corner_x, corner_y = x1, y2

    #generate tunnel coordinates
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y

def generate_dungeon(max_rooms, room_min, room_max, map_width, map_height, player) -> GameMap:
    """Generate a new dungeon map.

    Args:
        max_rooms (int): Maximum number of rooms
        room_min (int): Minimum room size
        room_max (int): Maximum room size
        map_width (int): Width of game map
        map_height (int): Height of game map
        player (Entity): Player entity

    Returns:
        dungeon: A new GameMap with rooms and tunnels
    """
    dungeon = GameMap(map_width,map_height, entities=[player])

    rooms: List[RectangularRoom] =[]
    
    for r in range(max_rooms):
        room_width = random.randint(room_min, room_max)
        room_height = random.randint(room_min, room_max)

        x = random.randint(0, dungeon.width - room_width -1)
        y = random.randint(0, dungeon.height - room_height -1)

        new_room = RectangularRoom(x, y, room_width, room_height)

        if any(new_room.intersects(other_room) for other_room in rooms):
            continue #this room intersects another, do not make it
        
        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) ==0:
            #the first room is where the player starts out
            player.x, player.y = new_room.center
        else:
            for x,y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x,y] = tile_types.floor
        
        rooms.append(new_room)

    return dungeon