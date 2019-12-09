import os
dirname = os.path.dirname(__file__)
input_txt = open(dirname + "/input.txt", "r").read()
input_list = list(map(int, input_txt.split(",")))

import itertools as itr
from typing import List


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
    def __init__(self, program: List[int], phase_setting: int):
        self.program = program[:]
        self.pointer = 0
        self.modes = 0
        self.inputs = [phase_setting]
        self.output = None
        self.new_output = False

    def should_halt(self):
        return self.pointer < 0

    def param(self, param_nb: int) -> int:
        """
            Applies the appropriate mode to the param at self.pointer + param_nb
            and returns the resulting value.
        """
        mode = get_digit_right_to_left(self.modes, param_nb - 1)
        param_index = self.pointer + param_nb
        return self.program[param_index] if mode == 1 else self.program[
            self.program[param_index]]

    def op_sum(self) -> None:
        storage_index = self.program[self.pointer + 3]
        self.program[storage_index] = self.param(1) + self.param(2)
        self.pointer += 4

    def op_multiply(self) -> None:
        storage_index = self.program[self.pointer + 3]
        self.program[storage_index] = self.param(1) * self.param(2)
        self.pointer += 4

    def op_input(self) -> None:
        value = self.inputs[0]
        self.inputs = self.inputs[1:]

        storage_index = self.program[self.pointer + 1]
        self.program[storage_index] = value
        self.pointer += 2

    def op_output(self) -> None:
        self.output = self.param(1)
        self.new_output = True
        self.pointer += 2

    def op_jump_if_true(self) -> None:
        self.pointer = self.param(2) if (
            self.param(1) != 0) else self.pointer + 3

    def op_jump_if_false(self) -> None:
        self.pointer = self.param(2) if (
            self.param(1) == 0) else self.pointer + 3

    def op_less_than(self) -> None:
        storage_index = self.program[self.pointer + 3]
        self.program[storage_index] = 1 if (
            self.param(1) < self.param(2)) else 0
        self.pointer += 4

    def op_equal_to(self) -> None:
        storage_index = self.program[self.pointer + 3]
        self.program[storage_index] = 1 if (
            self.param(1) == self.param(2)) else 0
        self.pointer += 4

    def parse_next_instruction(self) -> None:
        """
            Parses an instruction, executes it with the correct mode and returns
            the index of the next instruction or -1 if terminated.
        """
        instruction = self.program[self.pointer]
        opcode = instruction % 100

        if opcode == 99:
            self.pointer = -1

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

    def run_all(self, input_signal) -> None:
        self.inputs.append(input_signal)
        while not self.should_halt():
            self.parse_next_instruction()
        return self.output

    def run_to_next_output(self, new_input: int) -> int:
        self.inputs.append(new_input)
        while not (self.should_halt() or self.new_output):
            self.parse_next_instruction()
        self.new_output = False
        return self.output


class IntcodeCluster():
    def __init__(self,
                 program: List[int],
                 phase_setting: List[int],
                 loop: bool = False,
                 input_signal: int = 0):
        self.machines = [IntcodeComputer(program, ps) for ps in phase_setting]
        self.signal = input_signal
        self.counter = 0
        self.loop = loop

    def _run_once(self):
        for m in self.machines:
            self.signal = m.run_to_next_output(self.signal)
        return self.machines[4].output

    def _run_loop(self):
        while not self.machines[4].should_halt():
            self._run_once()
        return self.machines[4].output

    def run(self):
        return self._run_loop() if self.loop else self._run_once()


class SignalMaximizer():
    def __init__(self, loop: bool = False):
        phase_range = range(5, 10) if loop else range(0, 5)
        self.loop = loop
        self.phase_settings = list(itr.permutations(phase_range))
        self.max_output = 0

    def maximize(self, program: List[int]):
        for ps in self.phase_settings:
            cluster = IntcodeCluster(program, ps, self.loop)
            output = cluster.run()
            self.max_output = max((self.max_output, output))
        return self.max_output


sigmax = SignalMaximizer(False)
print(sigmax.maximize(input_list))
