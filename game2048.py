import random
import numpy


class Directions:
    UP = 1
    DOWN = 2
    RIGHT = 4
    LEFT = 8


class Field:

    def __init__(self) -> None:
        self.field = numpy.zeros((4, 4), dtype=int)
        self.chances = {
            2: 0.75,
            4: 0.20,
            8: 0.03,
            16: 0.015,
            32: 0.005
        }

    def start(self):
        self.spawn_node()
        self.spawn_node()

    def game_over(self):
        return numpy.count_nonzero(self.field) == 16

    def spawn_node(self):
        free_nodes = (self.field == 0).nonzero()
        coordinates = [(x, y) for x, y in zip(free_nodes[0], free_nodes[1])]
        coord = random.choice(coordinates)
        values = list(self.chances.keys())
        weights = list(self.chances.values())
        new_node = random.choices(values, weights)[0]
        self.field[coord] = new_node

    def action(self, direction):
        if direction == Directions.UP:
            self.field = numpy.rot90(self.field, k=1)
            self.merge_left()
            self.align_left()
            self.field = numpy.rot90(self.field, k=-1)
        if direction == Directions.DOWN:
            self.field = numpy.rot90(self.field, k=-1)
            self.merge_left()
            self.align_left()
            self.field = numpy.rot90(self.field, k=1)
        if direction == Directions.RIGHT:
            self.field = numpy.flip(self.field)
            self.merge_left()
            self.align_left()
            self.field = numpy.flip(self.field)
        if direction == Directions.LEFT:
            self.merge_left()
            self.align_left()

    def align_left(self):
        new = list()
        for i in range(len(self.field)):
            new_line = list()
            for j in range(len(self.field[i])):
                if self.field[i, j] != 0:
                    new_line.append(self.field[i, j])
            while len(new_line) < 4:
                new_line.append(0)
            new.append(new_line)
        self.field = numpy.asarray(new)

    def merge_left(self):
        for i in range(len(self.field)):
            for j in range(1, len(self.field[i])):
                a = self.field[i, j - 1]
                b = self.field[i, j]
                if a == b and a != 0:
                    self.field[i, j - 1] = a + b
                    self.field[i, j] = 0
