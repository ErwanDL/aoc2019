import os
dirname = os.path.dirname(__file__)
input_txt = open(dirname + "/input.txt", "r").read()
input_list = list(map(int, input_txt.split(",")))

from typing import List, Tuple, Dict
from collections import defaultdict, deque
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
    def __init__(self, program: List[int]):
        dict_program = {k: v for k, v in enumerate(program)}
        # storing the program using a defaultdict for easy auto-expansion
        self.program = defaultdict(lambda: 0, dict_program)
        self.pointer = 0
        self.modes = 0
        self.relative_base = 0
        self.halt = False
        self.input = None
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
        self.program[self.param(1)] = self.input
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

    def run_to_next_output(self, move_input: int) -> int:
        self.input = move_input
        while not (self.halt or self.new_output):
            self.parse_next_instruction()
        if self.halt:
            raise EndOfProgram()
        self.new_output = False
        return self.output


# TUPLE ARITHMETICS FUNCTIONS
def add(pos1: Tuple[int, int], pos2: Tuple[int, int]):
    return (pos1[0] + pos2[0], pos1[1] + pos2[1])


def substract(pos1: Tuple[int, int], pos2: Tuple[int, int]):
    return (pos1[0] - pos2[0], pos1[1] - pos2[1])


class Droid:
    # maps vector2 directions to the corresponding input instructions
    directions_mapping = {(1, 0): 4, (-1, 0): 3, (0, 1): 1, (0, -1): 2}

    def __init__(self, program: List[int]):
        self.cpt = IntcodeComputer(program)
        self.to_explore = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.current_position = (0, 0)
        self.previous_positions = []
        self.oxygen_position = None
        self.graph = defaultdict(lambda: [])

    def get_adjacent_vertices(self) -> List[Tuple[int, int]]:
        directions = Droid.directions_mapping.keys()
        return set([add(self.current_position, d) for d in directions])

    def create_graph_with_dfs(self) -> None:
        while len(self.to_explore) > 0:
            next_v = self.to_explore[-1]
            direction = substract(next_v, self.current_position)
            try:
                input_instr = Droid.directions_mapping[direction]
            except KeyError:
                # A KeyError is thrown if "direction" is not a unit direction vector :
                # this means that next_v is not adjacent to the current position.
                # This means that we have no more adjacent vertex to explore :
                # we can backtrack.
                prev_pos = self.previous_positions.pop()
                direction = substract(prev_pos, self.current_position)
                self.cpt.run_to_next_output(Droid.directions_mapping[direction])
                self.current_position = prev_pos
                continue

            self.to_explore.pop()
            result = self.cpt.run_to_next_output(input_instr)
            if result == 0:
                self.graph[next_v] = None
                continue

            if result == 2:
                print("found")
                self.oxygen_position = next_v

            # If we managed to move, we complete the graph by creating
            # an edge between current_position and next_v, and move the droid.
            self.graph[self.current_position].append(next_v)
            self.graph[next_v].append(self.current_position)
            self.previous_positions.append(self.current_position)
            self.current_position = next_v

            # Adding the adjacent unexplored vertices to the stack.
            next_vertices_to_explore = self.get_adjacent_vertices() - set(
                self.graph.keys())
            self.to_explore.extend(next_vertices_to_explore)

    def print_map(self) -> None:
        vertices = self.graph.keys()
        minRow, maxRow = min(vertices,
                             key=lambda x: x[1])[1], max(vertices,
                                                         key=lambda x: x[1])[1]
        minCol, maxCol = min(vertices,
                             key=lambda x: x[0])[0], max(vertices,
                                                         key=lambda x: x[0])[0]
        grid = np.full((maxRow - minRow + 1, maxCol - minCol + 1), "#")
        for v in vertices:
            if self.graph[v] != None:
                grid[v[1] - minRow, v[0] - minCol] = "."
        grid[-minRow, -minCol] = "D"
        grid[self.oxygen_position[1] - minRow,
             self.oxygen_position[0] - minCol] = "O"
        print(grid, grid.shape)

    def bfs_shortest_path(self) -> int:
        queue = deque([(0, 0)])
        visited_vertices = set()
        counter = 0
        while True:
            counter += 1
            next_ring = []
            while len(queue) > 0:
                next_v = queue.popleft()
                visited_vertices.add(next_v)
                if next_v == self.oxygen_position:
                    return counter
                next_ring.extend(set(self.graph[next_v]) - visited_vertices)
            queue.extend(next_ring)


np.set_printoptions(linewidth=200, threshold=5000)
droid = Droid(input_list)

droid.create_graph_with_dfs()
droid.print_map()
print(droid.bfs_shortest_path())