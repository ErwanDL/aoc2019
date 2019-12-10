from __future__ import annotations
import os
dirname = os.path.dirname(__file__)
input_txt = open(dirname + "/input.txt", "r").read()

import time
import math
from typing import Tuple, Dict

input_list = list(map(list, input_txt.split("\n")))


# defining functions for Vector2 arithmetics using tuples
def add(pos1: Tuple[int, int], pos2: tuple[int, int]):
    return (pos1[0] + pos2[0], pos1[1] + pos2[1])


def substract(pos1: Tuple[int, int], pos2: tuple[int, int]):
    return (pos1[0] - pos2[0], pos1[1] - pos2[1])


def mult(pos: Tuple[int, int], f: int):
    return (pos[0] * f, pos[1] * f)


def div(pos: Tuple[int, int], f: int):
    return (pos[0] / f, pos[1] / f)


class Asteroid():
    positions = {}

    def __init__(self, position: Tuple[int, int]):
        self.position = position
        self.detected_asteroids = set()

    def can_detect(self, other: Asteroid) -> Boolean:
        diff_vector = substract(other.position, self.position)
        gcd = math.gcd(diff_vector[0], diff_vector[1])

        # if gcd is 0, other is the same as self so we don't count it
        if gcd == 0:
            return False

        # if gcd is 1, no other asteroid can be on the line of sight : other is detected
        if gcd == 1:
            return True

        # if gcd is > 1, we check if any position in the line of sight has an asteroid
        elem_diff_vector = div(diff_vector, gcd)
        for i in range(1, gcd):
            pos_to_search = add(self.position, mult(elem_diff_vector, i))
            if pos_to_search in Asteroid.positions:
                return False
        return True

    def count_detectable_asteroids(self) -> int:
        for other in Asteroid.positions.values():
            # slightly optimizing by noticing that if A detects B, then B detects A
            if other not in self.detected_asteroids:
                if self.can_detect(other):
                    self.detected_asteroids.add(other)
                    other.detected_asteroids.add(self)
        return len(self.detected_asteroids)


tic = time.time()
for i in range(len(input_list[1])):
    for j in range(len(input_list[0])):
        if (input_list[j][i] == "#"):
            Asteroid.positions[i, j] = Asteroid((i, j))

counts = map(Asteroid.count_detectable_asteroids, Asteroid.positions.values())

print(max(counts))
toc = time.time()
print(toc - tic, "seconds")
