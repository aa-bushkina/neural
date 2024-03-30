import os
from math import floor
from random import random

import pygame

from config_variables import MAX_VEL, IMG_NAMES


class Car:
    x = 0
    y = 0

    # Положение машины относительно глобальной системы отсчета, координаты, угол поворота, скорость и ускорение
    def __init__(self, x, y, turn):
        self.x = x
        self.y = y
        self.rot = turn
        self.vel = MAX_VEL/2
        self.acc = 0
        self.initImgs()

    # Инициализация картинки машины
    def initImgs(self):
        name = IMG_NAMES[floor(random() * len(IMG_NAMES)) % len(IMG_NAMES)]
        self.img = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("imgs", name)).convert_alpha(), (120,69)), -90)