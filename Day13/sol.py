import os
dirname = os.path.dirname(__file__)
input_txt = open(dirname + "/input.txt", "r").read()
input_list = list(map(int, input_txt.split(",")))

from typing import List, Tuple, Dict, Callable
from collections import defaultdict
import numpy as np


def get_digit_right_to_left(number, digit_position):
    """
        Extracts from the input number the digit at the given position 
        from right to left, starting at 0.
    """
    if digit_position <= 0:
        return number % 10
    else:
        return get_digit_right_to_left(number // 10, digit_position - 1)


class EndOfProgram(Exception):
    pass


class IntcodeComputer:
    def __init__(self, program: List[int], input_callback: Callable):
        dict_program = {k: v for k, v in enumerate(program)}
        # storing the program using a defaultdict for easy auto-expansion
        self.program = defaultdict(lambda: 0, dict_program)
        self.pointer = 0
        self.modes = 0
        self.relative_base = 0
        self.halt = False
        self.input_callback = input_callback
        self.output = None
        self.new_output = False

    def param(self, param_nb: int) -> int:
        """
            Applies the appropriate mode to the param at self.pointer + param_nb
            and returns the index in the program at which to look.
        """
        mode = get_digit_right_to_left(self.modes, param_nb - 1)
        param_index = self.pointer + param_nb
        if mode == 1:
            # immediate mode
            return param_index
        if mode == 2:
            # relative mode
            return self.relative_base + self.program[param_index]
        else:
            # position mode
            return self.program[param_index]

    def op_sum(self) -> None:
        self.program[self.param(
            3)] = self.program[self.param(1)] + self.program[self.param(2)]
        self.pointer += 4

    def op_multiply(self) -> None:
        self.program[self.param(
            3)] = self.program[self.param(1)] * self.program[self.param(2)]
        self.pointer += 4

    def op_input(self) -> None:
        self.program[self.param(1)] = self.input_callback()
        self.pointer += 2

    def op_output(self) -> None:
        self.output = self.program[self.param(1)]
        self.new_output = True
        self.pointer += 2

    def op_jump_if_true(self) -> None:
        self.pointer = self.program[self.param(2)] if (
            self.program[self.param(1)] != 0) else self.pointer + 3

    def op_jump_if_false(self) -> None:
        self.pointer = self.program[self.param(2)] if (
            self.program[self.param(1)] == 0) else self.pointer + 3

    def op_less_than(self) -> None:
        self.program[self.param(3)] = 1 if (
            self.program[self.param(1)] < self.program[self.param(2)]) else 0
        self.pointer += 4

    def op_equal_to(self) -> None:
        self.program[self.param(3)] = 1 if (
            self.program[self.param(1)] == self.program[self.param(2)]) else 0
        self.pointer += 4

    def op_adjust_relative(self) -> None:
        self.relative_base += self.program[self.param(1)]
        self.pointer += 2

    def parse_next_instruction(self) -> None:
        """
            Parses an instruction, executes it with the correct mode and returns
            the index of the next instruction or -1 if terminated.
        """
        instruction = self.program[self.pointer]
        opcode = instruction % 100
        if opcode == 99:
            self.halt = True

        self.modes = instruction // 100

        if opcode == 1:
            self.op_sum()
        if opcode == 2:
            self.op_multiply()
        if opcode == 3:
            self.op_input()
        if opcode == 4:
            self.op_output()
        if opcode == 5:
            self.op_jump_if_true()
        if opcode == 6:
            self.op_jump_if_false()
        if opcode == 7:
            self.op_less_than()
        if opcode == 8:
            self.op_equal_to()
        if opcode == 9:
            self.op_adjust_relative()

    def run_all(self) -> None:
        while not self.halt:
            self.parse_next_instruction()
        return self.output

    def run_to_next_output(self) -> int:
        while not (self.halt or self.new_output):
            self.parse_next_instruction()
        if self.halt:
            raise EndOfProgram()
        self.new_output = False
        return self.output


class ArcadeCabinet:
    def get_auto_joystick_input(self) -> int:
        if self.ball_pos[0] > self.paddle_pos[0]:
            return 1
        if self.ball_pos[0] < self.paddle_pos[0]:
            return -1
        return 0

    def __init__(self, program: List[int]):
        self.cpt = IntcodeComputer(program, self.get_auto_joystick_input)
        self.cpt.program[0] = 2
        self.grid: Dict[Tuple[int, int], int] = {}
        self.score = 0
        self.paddle_pos: Tuple[int, int] = (0, 0)
        self.ball_pos: Tuple[int, int] = (0, 0)

    def get_next_triplet(self) -> List[int]:
        return [self.cpt.run_to_next_output() for i in range(3)]

    def parse_triplet(self, triplet: List[int]) -> bool:
        """
            Returns False if the triplet is a score indicator, or True if the
            triplet is a tile.
        """
        pos = tuple(triplet[:2])
        if pos == (-1, 0):
            self.score = triplet[2]
            return False
        if triplet[2] == 3:
            self.paddle_pos = pos
        elif triplet[2] == 4:
            self.ball_pos = pos
        self.grid[pos] = triplet[2]
        return True

    def draw_initial_grid(self) -> None:
        while self.parse_triplet(self.get_next_triplet()):
            pass

    def print_grid(self) -> None:
        coords = self.grid.keys()
        maxRow = max(coords, key=lambda x: x[1])[1]
        maxCol = max(coords, key=lambda x: x[0])[0]
        array_grid = np.zeros((maxRow + 1, maxCol + 1), dtype=int)
        for k in self.grid:
            array_grid[k[1], k[0]] = self.grid[k]
        print(array_grid)

    def get_nb_blocks(self) -> int:
        block_tiles = 0
        for k in self.grid:
            block_tiles += 1 * (self.grid[k] == 2)
        return block_tiles

    def play_game(self) -> int:
        while True:
            try:
                tilt = self.get_auto_joystick_input()
                self.cpt.input = tilt
                while self.parse_triplet(self.get_next_triplet()):
                    pass
            except EndOfProgram:
                break
        return self.score


np.set_printoptions(threshold=10000, linewidth=200)
arcade = ArcadeCabinet(input_list)
arcade.draw_initial_grid()
print(arcade.get_nb_blocks())
print(arcade.play_game())