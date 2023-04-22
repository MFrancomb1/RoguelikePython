from typing import Tuple

import numpy as np

graphic_dt = np.dtype(
    [
    ("ch", np.int32),
    ("fg", "3B"),
    ("bg", "3B"),
    ]
)