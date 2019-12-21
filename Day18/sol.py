import os
dirname = os.path.dirname(__file__)
input_txt = open(dirname + "/test.txt", "r").read()
input_list = input_txt.split("\n")
from typing import Dict, Tuple, List, Set
import numpy as np


# TUPLE ARITHMETICS FUNCTIONS
def add(pos1: Tuple[int, int], pos2: Tuple[int, int]):
    return (pos1[0] + pos2[0], pos1[1] + pos2[1])


def substract(pos1: Tuple[int, int], pos2: Tuple[int, int]):
    return (pos1[0] - pos2[0], pos1[1] - pos2[1])


class Labyrinth:
    @staticmethod
    def get_adjacent_vertices(current_position) -> List[Tuple[int, int]]:
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        return set([add(current_position, d) for d in directions])

    def __init__(self, input_lines: List[str]):
        shape = len(input_lines), len(input_lines[0])
        self.grid = {}
        self.keys = {}
        self.doors = {}
        for i in range(shape[0]):
            for j in range(shape[1]):
                val = input_lines[i][j]
                if val == "#":
                    continue
                elif val == "@":
                    self.start_pos = (i, j)
                    self.keys["@"] = (i, j)
                elif val.isalpha():
                    if val.islower():
                        self.keys[val] = (i, j)
                    else:
                        self.doors[val] = (i, j)
                self.grid[i, j] = val
        self.graph = {"@": []}

    def create_graph_dfs(self, current_pos: Tuple[int, int],
                         searched_vertices: Set[Tuple[int, int]],
                         previous_v: str, steps_since_previous_v: int,
                         doors_since_previous_v: List[str]) -> None:
        searched_vertices.add(current_pos)
        adj_vert = Labyrinth.get_adjacent_vertices(current_pos)
        to_search = []
        for v in adj_vert:
            if v in self.grid.keys() and v not in searched_vertices:
                # only search nodes that are in the grid, i.e. nodes that are
                # not '#'
                to_search.append(v)

        char = self.grid[current_pos]
        if char in self.keys or len(to_search) > 1:
            # if a key or an intersection is encountered, add it to the graph
            symbol = char if char in self.keys else str(current_pos)
            if previous_v != None:
                # previous_v is None at the very first step
                self.graph[symbol] = [(previous_v, steps_since_previous_v,
                                       doors_since_previous_v)]
                self.graph[previous_v].append(
                    (symbol, steps_since_previous_v, doors_since_previous_v))
            # the current node becomes the new "previous_v"
            previous_v = symbol
            steps_since_previous_v = 1
            doors_since_previous_v = []
        else:
            steps_since_previous_v += 1

        if char in self.doors:
            doors_since_previous_v.append(char)

        for v in to_search:
            self.create_graph_dfs(v, searched_vertices, previous_v,
                                  steps_since_previous_v,
                                  doors_since_previous_v)
        return

    def graph_without_intersections(self) -> Dict[str, List]:
        graph_wo = {}

        def get_key_neighbors_dfs(k, length_so_far: int, neighbors_dists: Dict,
                                  visited_neighbors: Set):
            for neighbor in self.graph[k]:
                if neighbor[0] in visited_neighbors:
                    continue
                else:
                    visited_neighbors.add(neighbor[0])
                    if neighbor[0].isalpha() or neighbor[0] == '@':
                        neighbors_dists[
                            neighbor[0]] = length_so_far + neighbor[1]
                    else:
                        print(k)
                        get_key_neighbors_dfs(neighbor[0],
                                              length_so_far + neighbor[1],
                                              neighbors_dists,
                                              visited_neighbors)
            return

        for k in self.graph:
            if k.isalpha() or k == '@':
                graph_wo[k] = {}
                get_key_neighbors_dfs(k, 0, graph_wo[k], set([k]))

        return graph_wo


laby = Labyrinth(input_list)
laby.create_graph_dfs(laby.start_pos, set(), None, 0, [])
print(laby.graph)
print(laby.graph_without_intersections())