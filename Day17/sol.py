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


def try_to_fill_with_patterns(l: List, index: int, patterns: Dict[str, List],
                              routine: List[str]):
    """
        We try to fill the rest of the original list with the patterns we have
        found so far. If, we do not succeed, we return False.
        In that case, we either have to try and add a new pattern (if our 
        patterns dict contains less than 3 patterns), or change our existing 
        patterns.
    """
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
                routine.append(p)
                index += len(to_try)
                break

        if not found_fitting_pattern:
            break
    if index == len(l):
        return True, index
    else:
        return False, index


def find_routine_and_patterns(l: List, max_characters=20):
    patterns = {}
    # i is the length of A, trying out with all possible lengths until
    # a correct routine is found
    for i in range(1, max_characters // 2 + 1):
        patterns["A"] = l[:i]
        routine = ["A"]

        # Try to fill the rest of the original list (after the first A) with
        # only A's, and if we can't add another A in a row, go and create a
        # B pattern.
        filled, start_first_b = try_to_fill_with_patterns(
            l, i, patterns, routine)
        routine_after_A = routine[:]

        # early return if the list is already filled (never happens)
        if filled:
            return routine, patterns

        for j in range(1, max_characters // 2 + 1):
            # always resetting the routine if previous attempt was unsuccessful
            routine = routine_after_A[:] + ["B"]
            patterns["B"] = l[start_first_b:start_first_b + j]

            # Try to fill the rest of the list (after the first B) with only A's
            # and B's, and if we can't add another A or B in a row, go and create
            # a C pattern.
            filled, start_first_c = try_to_fill_with_patterns(
                l, start_first_b + j, patterns, routine)
            routine_after_B = routine[:]

            # early return if the list is already filled (never happens)
            if filled:
                return routine, patterns

            for k in range(1, max_characters // 2 + 1):
                # always resetting the routine if previous attempt was unsuccessful
                routine = routine_after_B[:] + ["C"]
                patterns["C"] = l[start_first_c:start_first_c + k]
                index = start_first_c + k

                # Try and fill the rest of the list with only A's, B's and C's.
                # If it's not possible, it means we do not have the right A, B
                # and C patterns. In that case we try with other values of
                # i, j and k.
                if try_to_fill_with_patterns(l, index, patterns, routine)[0]:
                    return routine, patterns


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
        self.program = program[:]
        self.ASCII_repr = ASCIIparser.parse_to_ASCII(self.program)
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
        current_pos = self.robot_pos

        while True:
            possible_next_positions = []
            # Find what adjacent nodes are part of the scaffold
            for p in ASCIIparser.get_adjacent_pos(current_pos):
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
                    if substract(p, current_pos) == last_direction:
                        next_pos = p
                        break
            else:
                # Necessarily only 1 possible next position
                next_pos = possible_next_positions[0]

            direction = substract(next_pos, current_pos)

            if direction == last_direction:
                commands[-1] += 1
            elif (last_direction[1], -last_direction[0]) == direction:
                commands.extend(["R", 1])
            else:
                commands.extend(["L", 1])

            last_direction = direction
            visited_positions.append(current_pos)
            current_pos = next_pos
        return commands

    def wake_robot_and_collect_dust(self) -> int:
        self.program[0] = 2
        path_commands = self.path_to_visit_scaffold()
        routine, patterns = find_routine_and_patterns(path_commands)
        movement_rules = []

        def list_as_ASCII(l):
            output = []
            for element in l:
                for char in str(element):
                    output.append(ord(char))
                output.append(44)
            output.pop()
            output.append(10)
            return output

        movement_rules.extend(list_as_ASCII(routine))
        for p in patterns:
            movement_rules.extend(list_as_ASCII(patterns[p]))
        movement_rules.append(ord("n"))
        movement_rules.append(10)
        cpt = IntcodeComputer(self.program, movement_rules)
        res = cpt.run_all()
        return res


parser = ASCIIparser(input_list)
print(parser.ASCII_repr)
intersections = parser.find_scaffold_intersections()
sum_align_params = sum([row * col for row, col in intersections])
print("Sum of alignment parameters : {}".format(sum_align_params))

print("Commands in order to visit the whole scaffold : {}".format(
    parser.path_to_visit_scaffold()))
print("Res : {}".format(parser.wake_robot_and_collect_dust()))