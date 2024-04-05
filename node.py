from car import decode_command
from config_variables import *
from world import World


class Node:
    def __init__(self, id, x, y, type, color, label="", index=0):
        self.id = id
        self.x = x
        self.y = y
        self.type = type
        self.color = color
        self.label = label
        self.index = index

    def draw_node(self, world):
        colorScheme = self.get_node_colors(world)

        py.draw.circle(world.win, colorScheme[0], (self.x, self.y), NODE_RADIUS)
        py.draw.circle(world.win, colorScheme[1], (self.x, self.y), NODE_RADIUS - 2)

        if self.type != MIDDLE:
            text = NODE_FONT.render(self.label, 1, BLACK)
            world.win.blit(text, (
                self.x + (self.type - 1) * ((text.get_width() if not self.type else 0) + NODE_RADIUS + 5),
                self.y - text.get_height() / 2))

    def get_node_colors(self, world: World):

        if self.type == INPUT:
            ratio = world.best_inputs[self.index]
        elif self.type == OUTPUT:
            ratio = 1 if decode_command(world.best_commands, self.index) else 0
        else:
            ratio = 0

        col = [[0, 0, 0], [0, 0, 0]]
        for i in range(3):
            col[0][i] = int(ratio * (self.color[1][i] - self.color[3][i]) + self.color[3][i])
            col[1][i] = int(ratio * (self.color[0][i] - self.color[2][i]) + self.color[2][i])
        return col