import time
from typing import Tuple, List

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from PIL import Image, ImageDraw

from core import World, Ant
from simulator import Simulator

import constants as c
from utils import Point, rotation, TAU

from tqdm import tqdm


def show_world(world: World) -> np.ndarray:
    board = np.empty((world.size, world.size, 3))

    for i in range(world.size):
        for j in range(world.size):
            cell = world[i, j]
            if cell.food > 0:
                value = cell.food / c.FOOD_MAX
                color = [1, 1-value, 1-value]
            elif cell.food_pheromone > 0:
                value = cell.food_pheromone / c.PHEROMONE_SCALE
                color = [1-value, 1-value, 1]
            elif cell.home_pheromone > 0:
                value = cell.home_pheromone / c.PHEROMONE_SCALE
                color = [1-value, 1, 1-value]
            else:
                color = [1, 1, 1]

            board[i, j] = color

    board = np.array(board)
    board = (board * 255).astype(np.uint8)

    return board


def draw_ant(draw: ImageDraw.ImageDraw, ant: Ant):
    y, x = ant.location
    pos = (np.array([x, y]) + .5) * c.C2P
    rot = rotation(ant.direction * TAU / 8)
    start = rot @ np.array([c.C2P / 3, 0.]) + pos
    end = rot @ np.array([-c.C2P / 3, 0.]) + pos

    color = (255, 0, 0) if ant.food else (0, 0, 0)

    draw.line(start.tolist() + end.tolist(), fill=color, width=2)


def show_picture(world: World, ants: List[Ant]) -> Image:
    board = show_world(world)
    img = Image.fromarray(board)

    img = img.resize((c.RESOLUTION, c.RESOLUTION), resample=Image.NEAREST)

    # Draw a rectangle around the home
    draw = ImageDraw.Draw(img)

    draw.line((c.HOME_START * c.C2P, c.HOME_START * c.C2P) + (c.HOME_START * c.C2P, c.HOME_END * c.C2P),
              fill=(0, 0, 0), width=2)
    draw.line((c.HOME_START * c.C2P, c.HOME_START * c.C2P) + (c.HOME_END * c.C2P, c.HOME_START * c.C2P),
              fill=(0, 0, 0), width=2)
    draw.line((c.HOME_END * c.C2P, c.HOME_START * c.C2P) + (c.HOME_END * c.C2P, c.HOME_END * c.C2P),
              fill=(0, 0, 0), width=2)
    draw.line((c.HOME_START * c.C2P, c.HOME_END * c.C2P) + (c.HOME_END * c.C2P, c.HOME_END * c.C2P),
              fill=(0, 0, 0), width=2)

    for ant in ants:
        draw_ant(draw, ant)

    return img

