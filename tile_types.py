from typing import Tuple

import numpy as np

graphic_dt = np.dtype(
    [
    ("ch", np.int32),
    ("fg", "3B"), #3B = 3 unsigned bytes
    ("bg", "3B"),
    ]
)

tile_dt = np.dtype(
    [
        ("walkable", bool),  # True if this tile can be walked over.
        ("transparent", bool),  # True if this tile doesn't block FOV.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
        ("light", graphic_dt), # when the tile is in view
    ]
)

def new_tile(*, walkable: int, transparent: int, dark: Tuple[int, Tuple[int, int, int],Tuple[int, int, int]], light: Tuple[int, Tuple[int, int, int],Tuple[int, int, int]],) -> np.ndarray:
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)

#unexplored, unseen tiles are shrouded
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

floor = new_tile(
    walkable=True, transparent=True, dark=(ord(" "), (255, 255, 255), (50, 50, 150)), light=(ord(" "), (255, 255, 255), (200, 180, 50)),
)
wall = new_tile(
    walkable=False, transparent=False, dark=(ord(" "), (255, 255, 255), (0, 0, 100)), light=(ord(" "), (255, 255, 255), (130, 110, 50)),
)