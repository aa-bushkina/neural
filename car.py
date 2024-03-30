import os
from math import floor, sin, cos, radians
from random import random

import pygame

from config_variables import MAX_VEL, IMG_NAMES, BRAKE, ACC, TURN_LEFT, TURN_RIGHT, ACTIVATION_TRESHOLD, FRICTION, \
    ACC_STRENGTH, BRAKE_STRENGTH, TURN_VEL, MAX_VEL_REDUCTION


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

    # Двигаем и поварачиваем машину
    def move(self, t):
        self.acc = FRICTION

        if decodeCommand(self.commands, ACC):
            self.acc = ACC_STRENGTH
        if decodeCommand(self.commands, BRAKE):
            self.acc = -BRAKE_STRENGTH
        if decodeCommand(self.commands, TURN_LEFT):
            self.rot -= TURN_VEL
        if decodeCommand(self.commands, TURN_RIGHT):
            self.rot += TURN_VEL

        timeBuffer = 500
        if MAX_VEL_REDUCTION == 1 or t >= timeBuffer:
            max_vel_local = MAX_VEL
        else:
            ratio = MAX_VEL_REDUCTION + (1 - MAX_VEL_REDUCTION)*(t/timeBuffer)
            max_vel_local = MAX_VEL * ratio

        self.vel += self.acc
        if self.vel > max_vel_local:
            self.vel = max_vel_local
        if self.vel < 0:
            self.vel = 0
        self.x = self.x + self.vel * sin(radians(self.rot))
        self.y = self.y - self.vel * cos(radians(self.rot))

        return (self.x, self.y)


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