import os
from math import floor, sin, cos, radians, degrees, atan2
from math import *
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
        self.rotation = turn
        self.speed = MAX_SPEED / 2
        self.acc = 0
        self.init_images()
        self.commands = [0, 0, 0, 0]

    # Инициализация картинки машины
    def init_images(self):
        name = IMG_NAMES[floor(random() * len(IMG_NAMES)) % len(IMG_NAMES)]
        self.images = pygame.transform.rotate(
            pygame.transform.scale(pygame.image.load(os.path.join("images", name)).convert_alpha(), (120, 69)), -90)

    def get_inputs(self, world, road):
        sensors = []
        for k in range(8):
            sensors.append(SENSOR_DISTANCE)
        sensors_equations = get_sensor_equations(self, world)
        for v in [road.left_border_points, road.right_border_points]:
            i = road.bottom_point_index
            while v[i].y > self.y - SENSOR_DISTANCE:
                next_index = get_index(i + 1, NUM_POINTS * road.num_points)
                getDistance(self, sensors, sensors_equations, v[i], v[next_index])
                i = next_index
        if CAR_DBG:
            for k, s in enumerate(sensors):
                omega = radians(self.rotation + 45 * k)
                dx = s * sin(omega)
                dy = - s * cos(omega)
                if s < SENSOR_DISTANCE:
                    pygame.draw.circle(world.win, RED, world.get_screen_coords(self.x + dx, self.y + dy), 6)
        for s in range(len(sensors)):
            sensors[s] = 1 - sensors[s] / SENSOR_DISTANCE

        return sensors

    # Двигаем и поворачиваем машину
    def move(self, t):
        self.acc = FRICTION

        if decode_command(self.commands, ACC):
            self.acc = ACC_STRENGTH
        if decode_command(self.commands, BRAKE):
            self.acc = -BRAKE_STRENGTH
        if decode_command(self.commands, TURN_LEFT):
            self.rotation -= TURN_SPEED
        if decode_command(self.commands, TURN_RIGHT):
            self.rotation += TURN_SPEED

        timeBuffer = 500
        if MAX_VEL_REDUCTION == 1 or t >= timeBuffer:
            max_vel_local = MAX_SPEED
        else:
            ratio = MAX_VEL_REDUCTION + (1 - MAX_VEL_REDUCTION) * (t / timeBuffer)
            max_vel_local = MAX_SPEED * ratio

        self.speed += self.acc
        if self.speed > max_vel_local:
            self.speed = max_vel_local
        if self.speed < 0:
            self.speed = 0
        self.x = self.x + self.speed * sin(radians(self.rotation))
        self.y = self.y - self.speed * cos(radians(self.rotation))

        return (self.x, self.y)

    def draw(self, world):
        screen_position = world.get_screen_coords(self.x, self.y)
        rotated_img = pygame.transform.rotate(self.images, -self.rotation)
        new_rect = rotated_img.get_rect(center=screen_position)
        world.win.blit(rotated_img, new_rect.topleft)

    def detect_collision(self, road: Road):
        mask = pygame.mask.from_surface(self.images)
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


def get_sensor_equations(self, world):
    eq = []
    for i in range(4):
        omega = radians(self.rotation + 45 * i)
        dx = SENSOR_DISTANCE * sin(omega)
        dy = - SENSOR_DISTANCE * cos(omega)
        if CAR_DBG:
            pygame.draw.lines(world.win, GREEN, False, [world.get_screen_coords(self.x + dx, self.y + dy),
                                                        world.get_screen_coords(self.x - dx, self.y - dy)], 2)
        coef = getSegmentEquation(self, Coordinates(self.x + dx, self.y + dy))
        eq.append(coef)
    return eq


def getSegmentEquation(p, q):
    a = p.y - q.y
    b = q.x - p.x
    c = p.x * q.y - q.x * p.y
    return (a, b, c)


def getDistance(car, sensors, sensorsEquations, p, q):
    (a2, b2, c2) = getSegmentEquation(p, q)
    for i, (a1, b1, c1) in enumerate(sensorsEquations):
        if a1 != a2 or b1 != b2:
            d = b1 * a2 - a1 * b2
            if d == 0:
                continue
            y = (a1 * c2 - c1 * a2) / d
            x = (c1 * b2 - b1 * c2) / d
            if (y - p.y) * (y - q.y) > 0 or (x - p.x) * (x - q.x) > 0:
                continue
        else:
            (x, y) = (abs(p.x - q.x), abs(p.y - q.y))
        dist = ((car.x - x) ** 2 + (car.y - y) ** 2) ** 0.5
        omega = car.rotation + 45 * i
        alpha = 90 - degrees(atan2(car.y - y, x - car.x))
        if cos(alpha) * cos(omega) * 100 + sin(alpha) * sin(omega) * 100 > 0:
            index = i
        else:
            index = i + 4

        if dist < sensors[index]:
            sensors[index] = dist


# Декодируем команду нейронной сети
def decode_command(commands, type):
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
