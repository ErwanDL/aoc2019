import os
from typing import List
dirname = os.path.dirname(__file__)
input_txt = open(dirname + "/input.txt", "r").read()
input_list = list(map(lambda x: x.split(")"), input_txt.split("\n")))


class Node():
    # static dictionary that maps each planet name
    # to the corresponding Node object
    planets = {}

    def __init__(self, parent: str = None):
        self.parent = parent
        self.children: List[str] = []

    def add_child(self, child: str):
        self.children.append(child)


# creating the dictionary that gives all direct children for each planet
for pair in input_list:
    parent, child = pair
    if parent not in Node.planets:
        Node.planets[parent] = Node()
    Node.planets[parent].add_child(child)
    if child not in Node.planets:
        Node.planets[child] = Node(parent)
    else:
        Node.planets[child].parent = parent

planets_counts = dict.fromkeys(Node.planets.keys(), 0)


# depth first search of the resulting tree starting at COM to populate
# the dictionary that gives the number of indirect planets for each planet
def dfs(planet_name, count_so_far):
    if planet_name not in Node.planets:
        return

    for child in Node.planets[planet_name].children:
        planets_counts[child] = count_so_far + 1
        dfs(child, count_so_far + 1)
    return


# intializing DFS at "COM"
dfs("COM", 0)
# summing all indirect orbit counts
print(sum(planets_counts.values()))


def get_parents_chain(planet_name: str, parents_list: List[str]):
    parent_name = Node.planets[planet_name].parent
    if not parent_name:
        return
    parents_list.append(parent_name)
    get_parents_chain(parent_name, parents_list)
    return


YOU_parent_chain = []
SAN_parent_chain = []
get_parents_chain("YOU", YOU_parent_chain)
get_parents_chain("SAN", SAN_parent_chain)

index_closest_parent = -1
for i in range(1, max(len(YOU_parent_chain), len(SAN_parent_chain)) + 1):
    if YOU_parent_chain[-i] != SAN_parent_chain[-i]:
        break
    index_closest_parent += 1

print(
    len(YOU_parent_chain) + len(SAN_parent_chain) - 2 *
    (index_closest_parent + 1))
