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


def angle_between(v1: Tuple[int, int], v2: Tuple[int, int]) -> float:
    """
        Returns the angle (between 0 and 2*pi radians) of v2 wrt v1.
    """
    angle = math.atan2(v1[0] * v2[1] - v1[1] * v2[0],
                       v1[0] * v2[0] + v1[1] * v2[1])
    return angle if angle >= 0.0 else 2 * math.pi + angle


class Asteroid():
    positions = {}

    @staticmethod
    def populate_positions(data: List[List[str]]) -> None:
        for i in range(len(data[1])):
            for j in range(len(data[0])):
                if (data[j][i] == "#"):
                    Asteroid.positions[i, j] = Asteroid((i, j))

    @staticmethod
    def get_best_asteroid() -> Tuple[Asteroid, int]:
        counts = map(lambda x: (x, x.detect_asteroids()),
                     Asteroid.positions.values())
        return max(counts, key=lambda x: x[1])

    def __init__(self, position: Tuple[int, int]):
        self.position = position
        self.detected_asteroids = set()
        self.angle = None

    def __repr__(self):
        return "Asteroid at position " + str(self.position)

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

    def detect_asteroids(self) -> int:
        for other in Asteroid.positions.values():
            # slightly optimizing by noticing that if A detects B, then B detects A
            if other not in self.detected_asteroids:
                if self.can_detect(other):
                    self.detected_asteroids.add(other)
                    other.detected_asteroids.add(self)
        return len(self.detected_asteroids)

    def order_detected_by_angle(self) -> List[Asteroid]:
        for other in self.detected_asteroids:
            diff_vector = substract(other.position, self.position)
            other.angle = angle_between((0, -1), diff_vector)
        return sorted(self.detected_asteroids, key=lambda a: a.angle)

    def vaporize_detected_asteroids(self) -> None:
        print("Poof !")
        for other in self.detected_asteroids:
            del Asteroid.positions[other.position]
        self.detected_asteroids = set()

    def get_n_th_vaporized_asteroid(self, n: int) -> Asteroid:
        vaporized = 0
        while True:
            vaporizable = self.detect_asteroids()
            if vaporized + vaporizable >= n:
                return self.order_detected_by_angle()[n - vaporized - 1]
            self.vaporize_detected_asteroids()
            vaporized += vaporizable


tic = time.time()

Asteroid.populate_positions(input_list)
station, count = Asteroid.get_best_asteroid()
print("Number of detected asteroids from station at " + str(station.position) +
      " : " + str(count))
print("200th vaporized asteroid : " +
      str(station.get_n_th_vaporized_asteroid(200)))

toc = time.time()
print(toc - tic, "seconds")
