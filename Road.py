from scipy.interpolate import interpolate

from config_variables import *
import numpy as np
from math import *
from coordinates import *
from random import random, seed


# Дорога в игровом мире
class Road:
    def __init__(self, world):
        # Вычисление количества контрольных точек, основываясь на высоте окна мира и безопасном расстоянии
        self.num_points = (int)((world.win_height + SAFE_SPACE) / SPACING) + 2

        self.last_ctrl_point_index = 0
        self.points = []
        self.center_points = []
        self.left_border_points = []
        self.right_border_points = []

        # Создание списков контрольных точек
        for i in range(self.num_points):
            self.points.append(Coordinates())

        for i in range(NUM_POINTS * self.num_points):
            self.left_border_points.append(Coordinates(1000, 1000))
            self.right_border_points.append(Coordinates(1000, 1000))
            self.center_points.append(Coordinates(1000, 1000))

        # Инициализация первых двух контрольных точек и граничных точек
        self.points[0].set_coords(0, SPACING)
        self.points[1].set_coords(0, 0)
        for i in range(NUM_POINTS):
            x = self.points[0].x
            y = self.points[0].y - SPACING / NUM_POINTS * i
            self.center_points[i].set_coords(x, y)
            self.left_border_points[i].set_coords(x - ROAD_WIDTH / 2, y)
            self.right_border_points[i].set_coords(x + ROAD_WIDTH / 2, y)
        self.next_center_point_index = NUM_POINTS

        # Создание сегментов дороги между контрольными точками
        for i in range(self.num_points - 2):
            self.create_segment(i + 1)

        # Инициализация индексов
        self.last_ctrl_point_index = self.num_points - 1
        self.bottom_point_index = 0

    def calculate_borders(self, i):
        # Расчет координат граничных точек для указанной контрольной точки
        prev_index = get_index(i - 1, self.num_points * NUM_POINTS)
        center = self.center_points[i]
        prev = self.center_points[prev_index]
        angle = atan2(center.x - prev.x, prev.y - center.y)

        x = ROAD_WIDTH / 2 * cos(angle)
        y = ROAD_WIDTH / 2 * sin(angle)
        self.left_border_points[i].x = center.x - x
        self.left_border_points[i].y = center.y - y if not center.y - y >= self.left_border_points[prev_index].y else \
            self.left_border_points[prev_index].y
        self.right_border_points[i].x = center.x + x
        self.right_border_points[i].y = center.y + y if not center.y + y >= self.right_border_points[prev_index].y else \
            self.right_border_points[prev_index].y

    def create_segment(self, index):
        point1 = self.points[get_index(index, self.num_points)]
        point2 = self.points[get_index(index + 1, self.num_points)]

        # Задание координат и угла для следующей контрольной точки
        seed()
        point2.set_coords(point1.x + (random() - 0.5) * MAX_DEVIATION, point1.y - SPACING)
        point2.angle = MAX_ANGLE * (random() - 0.5)

        y_tmp = []
        for i in range(NUM_POINTS):
            y_tmp.append(point2.y + SPACING / NUM_POINTS * i)

        ny = np.array([point2.y, point1.y])
        nx = np.array([point2.x, point1.x])
        cs = interpolate.CubicSpline(ny, nx, axis=0, bc_type=((1, point2.angle), (1, point1.angle)))
        res = cs(y_tmp)

        for i in range(NUM_POINTS):
            self.center_points[self.next_center_point_index].x = res[NUM_POINTS - i - 1]
            self.center_points[self.next_center_point_index].y = y_tmp[NUM_POINTS - i - 1]
            self.calculate_borders(self.next_center_point_index)

            self.next_center_point_index = get_index(self.next_center_point_index + 1,
                                                     NUM_POINTS * self.num_points)

        self.last_ctrl_point_index = get_index(self.last_ctrl_point_index + 1, self.num_points)
        self.bottom_point_index = self.next_center_point_index


def get_index(i, cap):
    # Получение корректного индекса в пределах диапазона
    return (i + cap) % cap
