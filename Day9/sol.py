import os
dirname = os.path.dirname(__file__)
input_txt = open(dirname + "/input.txt", "r").read()
input_list = list(map(int, input_txt.split(",")))

import itertools as itr
from typing import List
from collections import defaultdict


def get_digit_right_to_left(number, digit_position):
    """
        Extracts from the input number the digit at the given position 
        from right to left, starting at 0.
    """
    if digit_position <= 0:
        return number % 10
    else:
        return get_digit_right_to_left(number // 10, digit_position - 1)


class IntcodeComputer():
    def __init__(self, program: List[int]):
        dict_program = {k: v for k, v in enumerate(program)}
        # storing the program using a defaultdict for easy auto-expansion
        self.program = defaultdict(lambda: 0, dict_program)
        self.pointer = 0
        self.modes = 0
        self.relative_base = 0
        self.halt = False

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
        value = int(input("Enter your input : "))

        self.program[self.param(1)] = value
        self.pointer += 2

    def op_output(self) -> None:
        self.output = self.program[self.param(1)]
        self.new_output = True
        print(self.output)
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


cpt = IntcodeComputer(input_list)

cpt.run_all()
