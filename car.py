import os
from math import floor, sin, cos, radians, degrees, atan2
from random import random

import pygame

from road import Road, get_index
from config_variables import *
from coordinates import Coordinates


class Car:
    x = 0
    y = 0

    # Положение машины относительно глобальной системы отсчета, координаты, угол поворота, скорость и ускорение
    def __init__(self, x, y, turn):
        self.x = x
        self.y = y
        self.rot = turn
        self.vel = MAX_VEL / 2
        self.acc = 0
        self.initImgs()
        self.commands = [0, 0, 0, 0]

    # Инициализация картинки машины
    def initImgs(self):
        name = IMG_NAMES[floor(random() * len(IMG_NAMES)) % len(IMG_NAMES)]
        self.img = pygame.transform.rotate(
            pygame.transform.scale(pygame.image.load(os.path.join("imgs", name)).convert_alpha(), (120, 69)), -90)

    def getInputs(self, world, road):
        sensors = []
        for k in range(8):
            sensors.append(SENSOR_DISTANCE)
        sensorsEquations = getSensorEquations(self, world)
        for v in [road.pointsLeft, road.pointsRight]:
            i = road.bottomPointIndex
            while v[i].y > self.y - SENSOR_DISTANCE:
                next_index = get_index(i+1, NUM_POINTS*road.num_ctrl_points)
                getDistance(self, sensors, sensorsEquations, v[i], v[next_index])
                i = next_index
        if CAR_DBG:
            for k,s in enumerate(sensors):
                omega = radians(self.rot + 45*k)
                dx = s * sin(omega)
                dy = - s * cos(omega)
                if s < SENSOR_DISTANCE:
                    pygame.draw.circle(world.win, RED, world.getScreenCoords(self.x+dx, self.y+dy), 6)
        for s in range(len(sensors)):
            sensors[s] = 1 - sensors[s]/SENSOR_DISTANCE

        return sensors

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
            ratio = MAX_VEL_REDUCTION + (1 - MAX_VEL_REDUCTION) * (t / timeBuffer)
            max_vel_local = MAX_VEL * ratio

        self.vel += self.acc
        if self.vel > max_vel_local:
            self.vel = max_vel_local
        if self.vel < 0:
            self.vel = 0
        self.x = self.x + self.vel * sin(radians(self.rot))
        self.y = self.y - self.vel * cos(radians(self.rot))

        return (self.x, self.y)

    def draw(self, world):
        screen_position = world.get_screen_coords(self.x, self.y)
        rotated_img = pygame.transform.rotate(self.img, -self.rot)
        new_rect = rotated_img.get_rect(center=screen_position)
        world.win.blit(rotated_img, new_rect.topleft)

    def detect_collision(self, road: Road):
        mask = pygame.mask.from_surface(self.img)
        (width, height) = mask.get_size()
        for v in [road.left_border_points, road.right_border_points]:
            for p in v:
                x = p.x - self.x + width / 2
                y = p.y - self.y + height / 2
                try:
                    if mask.get_at((int(x), int(y))):
                        return True
                except IndexError:
                    continue
        return False


def getSensorEquations(self, world):
    eq = []
    for i in range(4):
        omega = radians(self.rot + 45*i)
        dx = SENSOR_DISTANCE * sin(omega)
        dy = - SENSOR_DISTANCE * cos(omega)
        if CAR_DBG:
            pygame.draw.lines(world.win, GREEN, False, [world.getScreenCoords(self.x+dx, self.y+dy), world.getScreenCoords(self.x-dx, self.y-dy)], 2)
        coef = getSegmentEquation(self, Coordinates(self.x + dx, self.y + dy))
        eq.append(coef)
    return eq

def getSegmentEquation(p, q):
    a = p.y - q.y
    b = q.x -p.x
    c = p.x*q.y - q.x*p.y
    return (a,b,c)


def getDistance(car, sensors, sensorsEquations, p, q):
    (a2,b2,c2) = getSegmentEquation(p, q)
    for i,(a1,b1,c1) in enumerate(sensorsEquations):
        if a1!=a2 or b1!=b2:
            d = b1*a2 - a1*b2
            if d == 0:
                continue
            y = (a1*c2 - c1*a2)/d
            x = (c1*b2 - b1*c2)/d
            if (y-p.y)*(y-q.y) > 0 or (x-p.x)*(x-q.x) > 0:
                continue
        else:
            (x, y) = (abs(p.x-q.x), abs(p.y-q.y))
        dist = ((car.x - x)**2 + (car.y - y)**2)**0.5
        omega = car.rot +45*i
        alpha = 90- degrees(atan2(car.y - y, x-car.x))
        if cos(alpha)*cos(omega)*100 + sin(alpha)*sin(omega)*100 > 0:
            index = i
        else:
            index = i + 4

        if dist < sensors[index]:
            sensors[index] = dist


# Декодируем команду нейронной сети
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
