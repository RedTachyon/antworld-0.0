from collections import namedtuple
from enum import Enum
from typing import Any, Callable, List, Optional

import numpy as np


class Action(Enum):
    SEEK = 0
    DROP = 1
    TAKE = 2
    MOVE = 3
    LEFT = 4
    RIGHT = 5


class Point(namedtuple('Point', ['x', 'y'])):
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __sub__(self, other):
        return self + (-other)

TAU = 2 * np.pi

def rotation(theta: float) -> np.ndarray:
    c = np.cos(theta)
    s = np.sin(theta)
    return np.array([
        [c, s],
        [-s, c]
    ])


def normalize(vec: List[float], ignore: Optional[int] = None) -> List[float]:
    if ignore is None:
        total = sum(vec)
        n = len(vec)
        if total == 0:
            out = [1./n for _ in vec]
        else:
            out = [v / total for v in vec]
    else:
        total = sum([v for i, v in enumerate(vec) if i != ignore])
        n = len(vec) - 1
        if total == 0:
            out = [1./n for _ in vec]
        else:
            out = [v / total for v in vec]
        out[ignore] = 0.

    return out
