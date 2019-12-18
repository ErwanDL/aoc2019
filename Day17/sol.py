import os
dirname = os.path.dirname(__file__)
input_txt = open(dirname + "/input.txt", "r").read()
input_list = list(map(int, input_txt.split(",")))

from typing import List, Tuple, Dict, DefaultDict
from collections import defaultdict
from intcode_computer import IntcodeComputer, EndOfProgram

test_ASCII_repr = "#######...#####\n#.....#...#...#\n#.....#...#...#\n......#...#...#\n......#...###.#\n......#.....#.#\n^########...#.#\n......#.#...#.#\n......#########\n........#...#..\n....#########..\n....#...#......\n....#...#......\n....#...#......\n....#####......"


def substract(pos1: Tuple[int, int], pos2: Tuple[int, int]):
    return (pos1[0] - pos2[0], pos1[1] - pos2[1])


def find_patterns_in_list(l: List,
                          min_length=2,
                          multiple_of=1) -> List[Tuple[List, int]]:
    """
        Finds repeating patterns of given minimum length in the given list.
        If multiple_of is provided, it will only return patterns of size a
        a multiple of the provided value.
    """
    patterns = []
    for i in range(min_length, len(l) // 2):
        if i % multiple_of:
            continue
        print(i)
        for j in range(len(l) - i):
            pattern_to_search = l[j:j + i]
            count = 0
            for k in range(j, len(l) - i):
                if l[k:k + i] == pattern_to_search:
                    count += 1
            if count > 1:
                patterns.append((pattern_to_search, count))
    patterns.sort(key=lambda x: len(x) * x[1], reverse=True)
    return patterns


def try_to_fill_with_patterns(l, index, patterns, routine):
    # We try to fill the rest of the list with the existing patterns.
    while len(l) - index > 0:
        found_fitting_pattern = False
        for p in patterns:
            # We try the already existing patterns and if one of them matches
            # the next section of the list, we note that we have found
            # a fitting pattern.
            to_try = patterns[p]
            to_compare = l[index:index + len(to_try)]
            if to_try == to_compare:
                found_fitting_pattern = True
                print(routine)
                routine.append(p)
                index += len(to_try)
                break

        if not found_fitting_pattern:
            break
    if index == len(l):
        return True, index
    else:
        return False, index


def find_routine(l: List, max_characters=20):
    patterns = {}

    # We are first trying out all possible values of A, B and C as the
    # first 3 patterns.
    for i in range(1, max_characters // 2 + 1):
        patterns["A"] = l[:i]
        routine = ["A"]
        filled, start_first_b = try_to_fill_with_patterns(
            l, i, patterns, routine)
        routine_after_A = routine[:]
        if filled:
            return routine, patterns
        else:
            pass
        for j in range(1, max_characters // 2 + 1):
            routine = routine_after_A[:] + ["B"]
            patterns["B"] = l[start_first_b:start_first_b + j]
            filled, start_first_c = try_to_fill_with_patterns(
                l, start_first_b + j, patterns, routine)
            routine_after_B = routine[:]
            if filled:
                return routine, patterns
            else:
                pass
            for k in range(1, max_characters // 2 + 1):
                routine = routine_after_B[:] + ["C"]
                patterns["C"] = l[start_first_c:start_first_c + k]
                index = start_first_c + k

                if try_to_fill_with_patterns(l, index, patterns, routine)[0]:
                    return routine, patterns


test_list = [
    "R", 8, "R", 8, "R", 4, "R", 4, "R", 8, "L", 6, "L", 2, "R", 4, "R", 4, "R",
    8, "R", 8, "R", 8, "L", 6, "L", 2
]
test_list2 = [
    'L', 12, 'L', 6, 'L', 8, 'R', 6, 'L', 8, 'L', 8, 'R', 4, 'R', 6, 'R', 6,
    'L', 12, 'L', 6, 'L', 8, 'R', 6, 'L', 8, 'L', 8, 'R', 4, 'R', 6, 'R', 6,
    'L', 12, 'R', 6, 'L', 8, 'L', 12, 'R', 6, 'L', 8, 'L', 8, 'L', 8, 'R', 4,
    'R', 6, 'R', 6, 'L', 12, 'L', 6, 'L', 8, 'R', 6, 'L', 8, 'L', 8, 'R', 4,
    'R', 6, 'R', 6, 'L', 12, 'R', 6, 'L', 8
]

test_list3 = [1, 2, 4, 5, 1, 2, 9, 8, 1, 2]
print(find_routine(test_list2, 20))
"""
class ASCIIparser:
    @staticmethod
    def parse_to_ASCII(intcode: List[int]) -> str:
        cpt = IntcodeComputer(intcode)
        res = ""
        while True:
            try:
                res += chr(cpt.run_to_next_output())
            except EndOfProgram:
                break
        return res

    @staticmethod
    def ASCII_to_map(
        ASCII_rep: str
    ) -> Tuple[Dict[Tuple[int, int], str], Tuple[int, int], Tuple[int, int]]:
        map_repr = {}
        lines = ASCII_rep.split("\n")
        shape = (len(lines), len(lines[0]))
        robot_pos = None
        for i, l in enumerate(lines):
            for j, c in enumerate(l):
                if c in "#^v><":
                    map_repr[i, j] = c
                    if c != "#":
                        robot_pos = (i, j)
        return map_repr, shape, robot_pos

    @staticmethod
    def get_adjacent_pos(pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        row, col = pos
        return [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]

    def __init__(self, program: List[int]):
        self.ASCII_repr = ASCIIparser.parse_to_ASCII(program[:])
        #self.ASCII_repr = test_ASCII_repr
        self.map_repr, self.shape, self.robot_pos = ASCIIparser.ASCII_to_map(
            self.ASCII_repr)

    def find_scaffold_intersections(self) -> List[Tuple[int, int]]:
        intersections = []
        for pos in self.map_repr:
            try:
                for p in ASCIIparser.get_adjacent_pos(pos):
                    self.map_repr[p]
                intersections.append(pos)
            except KeyError:
                continue
        return intersections

    def path_to_visit_scaffold(self) -> List[str]:
        robot_orientations = {
            "^": (-1, 0),
            "v": (1, 0),
            ">": (0, 1),
            "<": (0, -1)
        }
        last_direction = robot_orientations[self.map_repr[self.robot_pos]]
        visited_positions = [None]
        commands = []

        while True:
            possible_next_positions = []
            # Find what adjacent nodes are part of the scaffold
            for p in ASCIIparser.get_adjacent_pos(self.robot_pos):
                try:
                    self.map_repr[p]
                    if p != visited_positions[-1]:
                        possible_next_positions.append(p)
                except KeyError:
                    continue
            if len(possible_next_positions) == 0:
                # This means we have reached the end of the scaffold
                break

            elif len(possible_next_positions) == 3:
                # If several options (when the robot is at an intersection),
                # prefer going forward.
                for p in possible_next_positions:
                    if substract(p, self.robot_pos) == last_direction:
                        next_pos = p
                        break
            else:
                # Necessarily only 1 possible next position
                next_pos = possible_next_positions[0]

            direction = substract(next_pos, self.robot_pos)

            if direction == last_direction:
                commands[-1] += 1
            elif (last_direction[1], -last_direction[0]) == direction:
                commands.extend(["R", 1])
            else:
                commands.extend(["L", 1])

            last_direction = direction
            visited_positions.append(self.robot_pos)
            self.robot_pos = next_pos
        print(len(commands))
        return commands


parser = ASCIIparser(input_list)
print(parser.ASCII_repr)
intersections = parser.find_scaffold_intersections()
sum_align_params = sum([row * col for row, col in intersections])

print(parser.path_to_visit_scaffold())"""