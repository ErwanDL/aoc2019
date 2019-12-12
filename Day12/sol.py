from __future__ import annotations
import os
from typing import List, Tuple
import numpy as np
import re
import math
from multiprocessing import Process, Pool
import time
dirname = os.path.dirname(__file__)
input_txt = open(dirname + "/input.txt", "r").read()

lines = input_txt.split("\n")
txt_positions = map(lambda s: re.sub("[^\d,-]", "", s).split(","), lines)
input_list = [tuple(map(int, coords)) for coords in txt_positions]


def lcm(*args):
    a = args[0]
    if len(args) <= 1:
        return a
    b = lcm(*args[1:])
    return abs(a * b) // math.gcd(a, b)


class Moon:
    @staticmethod
    def apply_gravity(a: Moon, b: Moon) -> None:
        for i in range(3):
            if a.pos[i] > b.pos[i]:
                a.vel[i] -= 1
                b.vel[i] += 1
            elif a.pos[i] < b.pos[i]:
                b.vel[i] -= 1
                a.vel[i] += 1

    def __init__(self, position: Tuple[int]):
        self.pos = np.array(position)
        self.vel = np.array((0, 0, 0))

    def __repr__(self) -> str:
        return "Pos({}, {}, {})\t\tVel({}, {}, {})".format(*self.pos, *self.vel)

    def apply_velocity(self) -> None:
        for i in range(3):
            self.pos[i] += self.vel[i]

    def potential_e(self) -> int:
        return sum(map(abs, self.pos))

    def kinetic_e(self) -> int:
        return sum(map(abs, self.vel))


class System:
    def __init__(self, moons_positions: List[Tuple[int]]):
        self.moons = [Moon(pos) for pos in moons_positions]
        self.initial_pos = np.array(moons_positions)

    def __repr__(self) -> str:
        res = ""
        for m in self.moons:
            res += str(m) + "\n"
        return res

    def one_step_sim(self) -> None:
        for m in range(len(self.moons)):
            for n in range(m):
                Moon.apply_gravity(self.moons[m], self.moons[n])

        for moon in self.moons:
            moon.apply_velocity()

    def n_steps_sim(self, n_steps=1000):
        for i in range(n_steps):
            self.one_step_sim()

    def total_e(self) -> int:
        total = 0
        for m in self.moons:
            total += m.potential_e() * m.kinetic_e()
        return total

    def get_pos_on_axis(self, axis: int) -> List[int]:
        return [m.pos[axis] for m in self.moons]

    def get_vel_on_axis(self, axis: int) -> List[int]:
        return [m.vel[axis] for m in self.moons]

    def get_cycle_length_on_axis(self, axis: int) -> int:
        min_cycle = 0
        counter = 0
        while not min_cycle:
            self.one_step_sim()
            counter += 1
            if (self.get_pos_on_axis(axis) == list(self.initial_pos[:, axis])
                    and self.get_vel_on_axis(axis) == [0, 0, 0, 0]):
                min_cycle = counter
        return min_cycle

    def get_cycle_length_multiprocess(self) -> int:
        p = Pool(processes=3)
        cycle_lengths = p.starmap(System.get_cycle_length_on_axis,
                                  [(self, i) for i in range(3)])
        p.close()
        return lcm(*cycle_lengths)

    def get_cycle_length_monoprocess(self) -> int:
        # min_cycle[0] will contain the minimum number of steps for the problem
        # to get back to its initial state on the X axis ; min_cycle[1] for the
        # Y axis ; min_cycle[2] for the Z axis
        min_cycles = [0, 0, 0]
        counter = 0

        while not (min_cycles[0] and min_cycles[1] and min_cycles[2]):
            counter += 1
            self.one_step_sim()
            for i in range(3):
                # checking (if not found yet) if the system on the i-th axis
                # has come back to its initial state
                if not min_cycles[i] and (
                        self.get_pos_on_axis(i) == list(self.initial_pos[:, i])
                        and self.get_vel_on_axis(i) == [0, 0, 0, 0]):
                    min_cycles[i] = counter

        return lcm(*min_cycles)


if __name__ == '__main__':
    syst = System(input_list)
    tic = time.time()
    print(syst.get_cycle_length_multiprocess())
    print(time.time() - tic)