from config_variables import MAX_VEL


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