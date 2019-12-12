from __future__ import annotations
import os
from typing import List, Tuple
import numpy as np
import re
import math
dirname = os.path.dirname(__file__)
input_txt = open(dirname + "/input.txt", "r").read()

lines = input_txt.split("\n")
txt_positions = map(lambda s: re.sub("[^\d,-]", "", s).split(","), lines)
input_list = [tuple(map(int, coords)) for coords in txt_positions]


def lcm(*args):
    if len(args) == 2:
        return abs(args[0] * args[1]) // math.gcd(args[0], args[1])
    else:
        return lcm(args[0], lcm(*args[1:]))


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

    def get_cycle_length(self) -> int:
        # min_cycle[0] will contain the minimum number of steps for the problem
        # to get back to its initial state on the X axis ; min_cycle[1] for the
        # Y axis ; min_cycle[2] for the Z axis
        min_cycle = [0, 0, 0]
        counter = 0

        while not (min_cycle[0] and min_cycle[1] and min_cycle[2]):
            counter += 1
            syst.one_step_sim()
            for i in range(3):
                # checking (if not found yet) if the system on the i-th axis
                # has come back to its initial state
                if not min_cycle[i] and (
                        syst.get_pos_on_axis(i) == list(syst.initial_pos[:, i])
                        and syst.get_vel_on_axis(i) == [0, 0, 0, 0]):
                    min_cycle[i] = counter

        return lcm(*min_cycle)


syst = System(input_list)
print(syst.get_cycle_length())
