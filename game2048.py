import random

import numpy as np


class Direction:
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Game2048:

    def __init__(self, uuid):
        self.uuid = uuid
        self.nodes = np.zeros((4, 4))
        self.items = [2, 4, 8, 16, 32, 64]
        self.chances = [90.0, 9.0, 0.4, 0.3, 0.2, 0.1]
        self.spawn()
        self.spawn()

    def as_dict(self):
        return {
            'uuid': str(self.uuid.int),
            'game_over': self.game_over
        }

    @property
    def game_over(self):
        if np.count_nonzero(self.nodes) == 16:
            return not self.merge_able()
        else:
            return False

    def spawn(self):
        random_index = random.choice(np.rot90(np.nonzero(self.nodes == 0)))
        x, y = random_index
        self.nodes[x, y] = random.choices(population=self.items, weights=self.chances)[0]

    def merge_able(self):
        merge = False
        merge = merge or self.merge_able_left()
        self.nodes = np.rot90(self.nodes)
        merge = merge or self.merge_able_left()
        self.nodes = np.rot90(self.nodes)
        merge = merge or self.merge_able_left()
        self.nodes = np.rot90(self.nodes)
        merge = merge or self.merge_able_left()
        self.nodes = np.rot90(self.nodes)
        return merge

    def merge_able_left(self):
        merge = False
        shape = self.nodes.shape
        for i in range(shape[0]):
            for j in range(1, shape[1]):
                v1 = self.nodes[i, j - 1]
                v2 = self.nodes[i, j]
                if v1 == v2:
                    merge = True
                    break
            if merge:
                break
        return merge

    def move(self, direction):
        match direction:
            case Direction.LEFT:
                self.merge_left()
                self.align_left()
            case Direction.RIGHT:
                self.nodes = np.flip(self.nodes)
                self.merge_left()
                self.align_left()
                self.nodes = np.flip(self.nodes)
            case Direction.UP:
                self.nodes = np.rot90(self.nodes, k=1)
                self.merge_left()
                self.align_left()
                self.nodes = np.rot90(self.nodes, k=-1)
            case Direction.DOWN:
                self.nodes = np.rot90(self.nodes, k=-1)
                self.merge_left()
                self.align_left()
                self.nodes = np.rot90(self.nodes, k=1)
        self.spawn()

    def merge_left(self):
        shape = self.nodes.shape
        for i in range(shape[0]):
            for j in range(1, shape[1]):
                v1 = self.nodes[i, j - 1]
                v2 = self.nodes[i, j]
                if v1 == v2:
                    self.nodes[i, j] = 0
                    self.nodes[i, j - 1] = v1 + v2

    def align_left(self):
        shape = self.nodes.shape
        for i in range(shape[0]):
            empty_index = 0
            for j in range(shape[1]):
                v = self.nodes[i, j]
                if v != 0:
                    self.nodes[i, j] = 0
                    self.nodes[i, empty_index] = v
                    empty_index = empty_index + 1
