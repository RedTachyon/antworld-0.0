import random
import time
from typing import List

from behavior import Optimizer, Actor
from core import World, Ant
from utils import Point, Action

import constants as c


class Simulator:
    world: World
    actors: List[Actor]

    def __init__(self):
        self.world = World(c.DIMENSIONS)
        self.actors = []

        for _ in range(c.FOOD_PLACES):
            self.world.sample().food = c.FOOD_MAX

        for i in c.HOME_RANGE:
            for j in c.HOME_RANGE:
                ant = Ant(Point(i, j), random.randint(0, 7))
                self.world[i, j].ant = ant
                self.world[i, j].home = True
                self.actors.append(Actor(self.world, ant))

    def iterate(self):
        for actor in self.actors:
            optimizer = Optimizer(actor.here, actor.nearby_places)

            if actor.foraging:
                action = optimizer.seek_food()
            else:
                action = optimizer.seek_home()

            if action == Action.DROP:
                actor.drop_food()
                actor.mark_food_trail()
                actor.turn(4)
            elif action == action.TAKE:
                actor.take_food()
                actor.mark_home_trail()
                actor.turn(4)
            elif action == Action.MOVE:
                actor.move()
            elif action == Action.LEFT:
                actor.turn(-1)
            elif action == Action.RIGHT:
                actor.turn(1)
            else:
                raise ValueError(f"{action} is not a valid action")
        self.evaporate()

    def evaporate(self):
        for cell, point in self.world.each():
            cell.home_pheromone *= c.EVAP_RATE
            if cell.home_pheromone <= 1e-2:
                cell.home_pheromone = 0.
            cell.food_pheromone *= c.EVAP_RATE
            if cell.food_pheromone <= 1e-2:
                cell.food_pheromone = 0.
