import random
from typing import Optional, Tuple, Generator

import numpy as np

from utils import Point


class Ant:
    location: Point
    direction: int
    food: bool

    def __init__(self, location: Point, direction: int):
        self.location = location
        self.direction = direction

        self.food = False


class Cell:
    location: Point
    food: int
    home_pheromone: float
    food_pheromone: float
    ant: Optional[Ant]
    home: bool

    def __init__(self, location: Point,
                 food: int = 0,
                 home_pheromone: float = 0.,
                 food_pheromone: float = 0.):
        self.location = location
        self.food = food
        self.home_pheromone = home_pheromone
        self.food_pheromone = food_pheromone

        self.ant = None
        self.home = False

    def __str__(self):
        return f"Cell at {self.location}; {self.food} {self.home_pheromone} {self.food_pheromone}"

    def __repr__(self):
        return str(self)


class World:
    def __init__(self, size: int):
        self.size = size
        self.data = [[Cell(Point(i, j)) for j in range(size)] for i in range(size)]

        # self.home_map = np.zeros((size, size))
        # self.h_pheromone = np.zeros((size, size))
        #
        # self.food_map = np.zeros((size, size))
        # self.f_pheromone = np.zeros((size, size))
        #
        # self.ant_map = [[None for _ in range(size)] for _ in range(size)]

    def __getitem__(self, item: Tuple[int, int]) -> Cell:
        x, y = item
        return self.data[x][y]

    def __str__(self):
        return f"<{self.size}x{self.size} world>"

    def sample(self) -> Cell:
        return self[random.randint(0, self.size - 1), random.randint(0, self.size - 1)]

    def each(self) -> Generator[Cell, None, None]:
        for i in range(self.size):
            for j in range(self.size):
                yield self[i, j], Point(i, j)