class Coordinates:
    def __init__(self, x=-1, y=-1, angle=0):
        self.x = x
        self.y = y
        self.angle = angle

    def int(self, x, y):
        self.x = x
        self.y = y

    def get(self):
        return self.x, self.y
