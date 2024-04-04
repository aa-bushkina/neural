import pygame as py


class World:
    initial_pos = (0, 0)

    def __init__(self, starting_pos, world_width, world_height):
        self.initial_pos = starting_pos
        self.best_car_pos = (0, 0)
        self.win = py.display.set_mode((world_width, world_height))
        self.win_width = world_width
        self.score = 0
        self.win_height = world_height

    def get_screen_coords(self, x, y):
        return int(x + self.initial_pos[0] - self.best_car_pos[0]), int(y + self.initial_pos[1] - self.best_car_pos[1])

    def update_score(self, new_score):
        self.score = new_score

    def update_best_car_pos(self, pos):
        self.best_car_pos = pos

    def get_best_car_pos(self):
        return self.best_car_pos

    def get_score(self):
        return self.score
