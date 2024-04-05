from config_variables import *


class Connection:
    def __init__(self, input, output, weight):
        self.input = input
        self.output = output
        self.weight = weight

    def draw_connection(self, world):
        color = GREEN if self.weight >= 0 else RED
        width = int(abs(self.weight * CONNECTION_WIDTH))
        py.draw.line(world.win, color, (self.input.x + NODE_RADIUS, self.input.y),
                     (self.output.x - NODE_RADIUS, self.output.y), width)
