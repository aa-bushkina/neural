import pygame as py


class World:
    initialPos = (0, 0)

    def __init__(self, starting_pos, world_width, world_height):
        self.initialPos = starting_pos
        self.bestCarPos = (0, 0)
        self.win = py.display.set_mode((world_width, world_height))
        self.win_width = world_width
        self.win_height = world_height

    def get_screen_coords(self, x, y):
        return int(x + self.initialPos[0] - self.bestCarPos[0]), int(y + self.initialPos[1] - self.bestCarPos[1])
