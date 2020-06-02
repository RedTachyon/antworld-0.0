from typing import Set, Tuple, List

import numpy as np

from core import World, Ant, Cell
from utils import Point, Action, normalize


class Actor:
    DIR_DELTA = [(0, -1),
                 (1, -1),
                 (1, 0),
                 (1, 1),
                 (0, 1),
                 (-1, 1),
                 (-1, 0),
                 (-1, -1)]

    def __init__(self, world: World, ant: Ant):
        self.world = world
        self.ant = ant

        self.history: Set[Cell] = set()

    def turn(self, amount: int):
        self.ant.direction = (self.ant.direction + amount) % 8

    def move(self):
        self.history.add(self.here)

        new_location = self.neighbor(self.ant.direction)

        self.here.ant = None
        self.ahead.ant = self.ant

        self.ant.location = new_location

    @property
    def here(self) -> Cell:
        return self.world[self.ant.location]

    @property
    def ahead(self) -> Cell:
        return self.world[self.neighbor(self.ant.direction)]

    @property
    def ahead_left(self) -> Cell:
        return self.world[self.neighbor((self.ant.direction - 1) % 8)]

    @property
    def ahead_right(self) -> Cell:
        return self.world[self.neighbor((self.ant.direction + 1) % 8)]

    @property
    def nearby_places(self) -> Tuple[Cell, Cell, Cell]:
        return self.ahead_left, self.ahead, self.ahead_right

    def neighbor(self, direction: int) -> Point:
        x, y = self.ant.location
        dx, dy = self.DIR_DELTA[direction]
        assert direction in range(8)
        return Point((x + dx) % self.world.size, (y + dy) % self.world.size)

    def drop_food(self):
        self.here.food += 1
        self.ant.food = False

    def take_food(self):
        self.here.food -= 1
        self.ant.food = True

    def mark_food_trail(self):
        for old_cell in self.history:
            if old_cell.food == 0:
                old_cell.food_pheromone += 1

        self.history.clear()

    def mark_home_trail(self):
        for old_cell in self.history:
            if old_cell.home == 0:
                old_cell.home_pheromone += 1

        self.history.clear()

    @property
    def foraging(self):
        return not self.ant.food


class Optimizer:
    BEST_CHOICE_BONUS = 3

    here: Cell
    nearby_places: Tuple[Cell, Cell, Cell]
    ahead_left: Cell
    ahead: Cell
    ahead_right: Cell

    def __init__(self, here: Cell, nearby_places: Tuple[Cell, Cell, Cell]):
        self.here = here
        self.nearby_places = nearby_places

        self.ahead_left, self.ahead, self.ahead_right = self.nearby_places

    def seek_food(self) -> Action:
        if self.here.food > 0 and not self.here.home:
            return Action.TAKE
        elif self.ahead.food > 0 and not self.ahead.home and not self.ahead.ant:
            return Action.MOVE
        else:
            return self.follow_trail(home=False)

    def seek_home(self) -> Action:
        if self.here.home:
            return Action.DROP
        elif self.ahead.home and not self.ahead.ant:
            return Action.MOVE
        else:
            return self.follow_trail(home=True)

    def follow_trail(self, home: bool = False) -> Action:
        if home:
            ranking = [place.home + place.home_pheromone for place in self.nearby_places]
        else:
            ranking = [place.food + place.food_pheromone for place in self.nearby_places]

        best_idx = int(np.argmax(ranking))
        ranking[best_idx] *= self.BEST_CHOICE_BONUS

        ignore = 1 if self.ahead.ant else None
        probs = normalize(ranking, ignore)

        choice = np.random.choice(range(len(probs)), p=probs)

        return [Action.LEFT, Action.MOVE, Action.RIGHT][choice]
