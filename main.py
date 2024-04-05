import neat
import os
from car import Car
from road import Road
from world import World
from NNdraw import NN
from config_variables import *

py.font.init()
background = py.Surface((WIN_WIDTH, WIN_HEIGHT))
background.fill(WHITE)


def draw_win(cars, road, world, GEN):
    road.draw(world)
    for car in cars:
        car.draw(world)

    text = STAT_FONT.render("Пройденная дистанция: " + str(int(world.get_score())), 1, BLACK)
    world.win.blit(text, (world.win_width - text.get_width() - 10, 10))
    text = STAT_FONT.render("Поколение: " + str(GEN), 1, BLACK)
    world.win.blit(text, (world.win_width - text.get_width() - 10, 50))

    world.bestNN.draw(world)

    py.display.update()
    world.win.blit(background, (0, 0))


def main(genomes=[], config=[]):
    global GENERATION_COUNTER
    GENERATION_COUNTER += 1

    nets = []
    genoms = []
    cars = []
    time = 0

    world = World(STARTING_POS, WIN_WIDTH, WIN_HEIGHT)
    world.win.blit(background, (0, 0))

    NNs = []

    for _, genom in genomes:
        net = neat.nn.FeedForwardNetwork.create(genom, config)
        nets.append(net)
        cars.append(Car(0, 0, 0))
        genom.fitness = 0
        genoms.append(genom)
        NNs.append(NN(config, genom, (90, 210)))

    road = Road(world)
    clock = py.time.Clock()

    run = True
    while run:
        time += 1
        clock.tick(FPS)
        world.update_score(0)

        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                py.quit()
                quit()

        (xb, yb) = (0, 0)
        i = 0
        while i < len(cars):
            car = cars[i]

            input = car.get_inputs(world, road)
            input.append(car.speed / MAX_SPEED)
            car.commands = nets[i].activate(tuple(input))

            y_old = car.y
            (x, y) = car.move(time)

            if time > 10 and (car.detect_collision(road) or y > world.get_best_car_pos()[
                1] + BAD_GENOME_TRESHOLD or y > y_old or car.speed < 0.1):
                genoms[i].fitness -= 1
                cars.pop(i)
                nets.pop(i)
                genoms.pop(i)
                NNs.pop(i)
            else:
                genoms[i].fitness += -(y - y_old) / 100 + car.speed * SCORE_SPEED_MULTIPLIER
                if genoms[i].fitness > world.get_score():
                    world.update_score(genoms[i].fitness)
                    world.bestNN = NNs[i]
                    world.best_inputs = input
                    world.best_commands = car.commands
                i += 1

            if y < yb:
                (xb, yb) = (x, y)

        if len(cars) == 0:
            run = False
            break

        world.update_best_car_pos((xb, yb))
        road.update(world)
        draw_win(cars, road, world, GENERATION_COUNTER)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.run(main, 10000)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config_file.txt")
    run(config_path)
