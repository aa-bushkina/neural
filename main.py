from world import World
from config_variables import *
import pygame as py

background = py.Surface((WIN_WIDTH, WIN_HEIGHT))
background.fill(GRAY)


def draw(world):
    py.display.update()
    world.win.blit(background, (0, 0))


def main():
    t = 0

    world = World(STARTING_POS, WIN_WIDTH, WIN_HEIGHT)
    world.win.blit(background, (0, 0))

    clock = py.time.Clock()

    run = True
    while run:
        t += 1
        clock.tick(FPS)

        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                py.quit()
                quit()

        draw(world)


if __name__ == "__main__":
    main()
