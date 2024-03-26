import pygame as py


class World:
    initialPos = (0, 0)

    def __init__(self, starting_pos, world_width, world_height):
        self.initialPos = starting_pos
        self.win = py.display.set_mode((world_width, world_height))
        self.win_width = world_width
        self.win_height = world_height
