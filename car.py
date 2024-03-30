import os
from math import floor
from random import random

import pygame

from config_variables import MAX_VEL, IMG_NAMES, BRAKE, ACC, TURN_LEFT, TURN_RIGHT, ACTIVATION_TRESHOLD


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
        self.commands = [0,0,0,0]

    # Инициализация картинки машины
    def initImgs(self):
        name = IMG_NAMES[floor(random() * len(IMG_NAMES)) % len(IMG_NAMES)]
        self.img = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("imgs", name)).convert_alpha(), (120,69)), -90)

    # Деккодируем команду нейронной сети
    def decodeCommand(commands, type):
        if commands[type] > ACTIVATION_TRESHOLD:
            if type == ACC and commands[type] > commands[BRAKE]:
                return True
            elif type == BRAKE and commands[type] > commands[ACC]:
                return True
            elif type == TURN_LEFT and commands[type] > commands[TURN_RIGHT]:
                return True
            elif type == TURN_RIGHT and commands[type] > commands[TURN_LEFT]:
                return True
        return False