import neat
import os
from car import Car
from road import Road
from world import World
from NNdraw import NN
from config_variables import *

py.font.init()
background = py.Surface((WIN_WIDTH, WIN_HEIGHT))
background.fill(GRAY)

def draw_win(cars, road, world, GEN):
    road.draw(world)
    for car in cars:
        car.draw(world)

    text = STAT_FONT.render("Best Car Score: "+str(int(world.getScore())), 1, BLACK)
    world.win.blit(text, (world.win_width-text.get_width() - 10, 10))
    text = STAT_FONT.render("Gen: "+str(GEN), 1, BLACK)
    world.win.blit(text, (world.win_width-text.get_width() - 10, 50))

    world.bestNN.draw(world)

    py.display.update()
    world.win.blit(background, (0,0))

def main(genomes = [], config = []):
    global GEN
    GEN += 1

    nets = []
    ge = []
    cars = []
    t = 0

    world = World(STARTING_POS, WIN_WIDTH, WIN_HEIGHT)
    world.win.blit(background, (0,0))

    NNs = []

    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        cars.append(Car(0, 0, 0))
        g.fitness = 0
        ge.append(g)
        NNs.append(NN(config, g, (90, 210)))

    road = Road(world)
    clock = py.time.Clock()

    run = True
    while run:
        t += 1
        clock.tick(FPS)
        world.updateScore(0)

        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                py.quit()
                quit()

        (xb, yb) = (0,0)
        i = 0
        while(i < len(cars)):
            car = cars[i]

            input = car.getInputs(world, road)
            input.append(car.vel/MAX_VEL)
            car.commands = nets[i].activate(tuple(input))

            y_old = car.y
            (x, y) = car.move(t)

            if y < yb:
                (xb, yb) = (x, y)


        if len(cars) == 0:
            run = False
            break

        world.updateBestCarPos((xb, yb))
        road.update(world)
        draw_win(cars, road, world, GEN)

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats =neat.StatisticsReporter()
    p.add_reporter(stats)
    p.run(main, 10000)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config_file.txt")
    run(config_path)
