import os
dirname = os.path.dirname(__file__)
input_txt = open(dirname + "/test2.txt", "r").read()
input_list = input_txt.split("\n")
from typing import Dict, Tuple, List, Set
import numpy as np
import math
import itertools


# TUPLE ARITHMETICS FUNCTIONS
def add(pos1: Tuple[int, int], pos2: Tuple[int, int]):
    return (pos1[0] + pos2[0], pos1[1] + pos2[1])


def substract(pos1: Tuple[int, int], pos2: Tuple[int, int]):
    return (pos1[0] - pos2[0], pos1[1] - pos2[1])


def dijkstra(graph, start_key: str) -> Dict[str, int]:
    shortest_paths = {k: {"path": [], "dist": math.inf} for k in graph.keys()}
    shortest_paths[start_key]["dist"] = 0

    def update_distance(v1: str, v2: str, dist_v1_to_v2: int):
        new_dist = shortest_paths[v1]["dist"] + dist_v1_to_v2
        if shortest_paths[v2]["dist"] > new_dist:
            shortest_paths[v2]["dist"] = new_dist
            shortest_paths[v2]["path"] = shortest_paths[v1]["path"] + [v2]

    def select_next_vertex(vertices_to_visit):
        min_dist, best_v = math.inf, None
        for v in vertices_to_visit:
            dist = shortest_paths[v]["dist"]
            if dist < min_dist:
                min_dist = dist
                best_v = v
        return best_v

    vertices_to_visit = set(graph.keys())
    next_vertices = []

    while len(vertices_to_visit) > 0:
        next_v = select_next_vertex(vertices_to_visit)
        vertices_to_visit.remove(next_v)
        for neigh, (dist, path) in graph[next_v].items():
            update_distance(next_v, neigh, dist)

    return shortest_paths


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
        self.graph = {'@': {}}
        """ self.graph = {
            "@": {
                '(39, 40)': (1, []),
                '(41, 40)': (1, []),
                '(40, 39)': (1, []),
                '(40, 41)': (1, []),
            },
            "(39, 40)": {
                "@": (1, [])
            },
            "(41, 40)": {
                "@": (1, [])
            },
            "(40, 39)": {
                "@": (1, [])
            },
            "(40, 41)": {
                "@": (1, [])
            }
        } """

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
                self.graph[symbol] = {
                    previous_v:
                    (steps_since_previous_v, doors_since_previous_v[:])
                }
                self.graph[previous_v][symbol] = (steps_since_previous_v,
                                                  doors_since_previous_v[:])
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

    def graph_without_intersections(self) -> Dict[str, List]:
        graph_wo = {}

        def get_key_neighbors_dfs(k, length_so_far: int, neighbors_dists: Dict,
                                  visited_neighbors: Set):
            """
                Retrieves the direct neighbor KEYS (not intersections) of a 
                certain Key, and the distance to this initial Key.
            """
            for neighbor, (dist, _) in self.graph[k].items():
                if neighbor in visited_neighbors:
                    continue
                else:
                    visited_neighbors.add(neighbor)
                    if neighbor.isalpha() or neighbor == '@':
                        neighbors_dists[neighbor] = length_so_far + dist
                    else:
                        get_key_neighbors_dfs(neighbor, length_so_far + dist,
                                              neighbors_dists,
                                              visited_neighbors)

        for k in self.graph:
            if k.isalpha() or k == '@':
                graph_wo[k] = {}
                get_key_neighbors_dfs(k, 0, graph_wo[k], set([k]))
        self.simplified_graph = graph_wo
        return graph_wo

    def keys_prerequisites(self) -> Dict[str, List[str]]:
        def find_prereq_doors(current_key: str, doors_so_far: List[str],
                              visited_vertices: Set[str],
                              prerequisites: Dict[str, List[str]]):
            visited_vertices.add(current_key)
            if current_key.isalpha() or current_key == "@":
                prerequisites[current_key] = doors_so_far
            to_visit = self.graph[current_key]
            for v, (_, doors) in to_visit.items():
                if v in visited_vertices:
                    continue
                next_doors_so_far = doors_so_far[:]
                next_doors_so_far.extend(doors)
                find_prereq_doors(v, next_doors_so_far, visited_vertices,
                                  prerequisites)
            return prerequisites

        prereq_doors = find_prereq_doors("@", [], set(),
                                         dict.fromkeys(self.keys.keys()))

        def find_prereq_keys(current_key: str, prereq_keys: Dict[str,
                                                                 Set[str]]):
            prerequisites = set()
            for door in prereq_doors[current_key]:
                associated_key = door.lower()
                prerequisites.add(associated_key)
                if associated_key not in prereq_keys:
                    find_prereq_keys(associated_key, prereq_keys)
                prerequisites.update(prereq_keys[associated_key])
            prereq_keys[current_key] = prerequisites
            return prereq_keys

        prereq_keys = {}
        for k in prereq_doors:
            find_prereq_keys(k, prereq_keys)

        self.prereq_keys = prereq_keys
        return prereq_keys

    def compute_shortest_paths(self):
        self.shortest_paths = dict.fromkeys(self.keys)
        for k in self.keys:
            self.shortest_paths[k] = dijkstra(self.graph, k)

    def tsp_brute_force(self,
                        current_key: str,
                        keys_in_pocket: List[str],
                        shortest_so_far=0) -> Tuple[int, List[str]]:
        if len(keys_in_pocket) == len(self.keys):
            return shortest_so_far, keys_in_pocket
        else:
            possibilities_next_key = [
                k for k in self.keys
                if (k not in keys_in_pocket
                    and self.prereq_keys[k].issubset(set(keys_in_pocket)))
            ]
            next_min = math.inf
            best_path = None

            for k in possibilities_next_key:
                path_dist_to_k = self.shortest_paths[current_key][k]
                next_keys_in_pocket = keys_in_pocket.copy()
                next_keys_in_pocket.extend([
                    k for k in path_dist_to_k["path"]
                    if (k in self.keys and k not in keys_in_pocket)
                ])
                next_dist, path = self.tsp_brute_force(
                    k, next_keys_in_pocket,
                    shortest_so_far + path_dist_to_k["dist"])
                if next_dist < next_min:
                    next_min = next_dist
                    best_path = path
            return next_min, best_path

    def tsp_dynamic(self):
        # C will hold at key (i, {a, b, c...}) the shortest path from start
        # to vertex i that passes by all the vertices {a, b, c...}
        C = {}
        keys_wo_start = set(self.keys) - {'@'}
        for i in keys_wo_start:
            C[frozenset({i}), i] = self.shortest_paths['@'][i]
        for s in range(2, len(self.keys)):
            size_s_sets = list(itertools.combinations(keys_wo_start, s))
            for s_set in size_s_sets:
                for k in keys_wo_start:
                    subproblems = [
                        C[frozenset(s_set - {k}, m)] + self.shortest_paths[m][k]
                        for m in keys_wo_start if m != k
                    ]
                    C[frozenset(s_set), k] = min()
        return


laby = Labyrinth(input_list)
laby.create_graph_dfs(laby.start_pos, set(laby.graph.keys()), None, 0, [])
laby.compute_shortest_paths()
laby.keys_prerequisites()
print(laby.graph)
print(laby.tsp_brute_force("@", ['@']))