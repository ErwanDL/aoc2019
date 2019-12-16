import os
dirname = os.path.dirname(__file__)
from typing import List, Tuple, DefaultDict
from collections import defaultdict
import math
input_txt = open(dirname + "/input.txt", "r").read()


class Material:
    def __init__(self, name: str, quantity_per_batch: int,
                 recipe: List[Tuple[int, str]]):
        self.name = name
        self.quantity_per_batch = quantity_per_batch
        self.recipe = recipe

    def __repr__(self) -> str:
        res = "{} of Material {} requires ".format(self.quantity_per_batch,
                                                   self.name)
        for i in self.recipe[:-1]:
            res += "{} {}, ".format(i[0], i[1])
        res += "{} {}.\n".format(self.recipe[-1][0], self.recipe[-1][1])
        return res


materials = {}


def parse_input(s: str):
    lines = [l.split(" => ") for l in s.split("\n")]
    for l in lines:
        recipe = [tuple(i.split(" ")) for i in l[0].split(", ")]
        quantity, product = l[1].split(" ")
        materials[product] = Material(product, int(quantity), recipe)


def dfs(
    req_quantity: int = 1,
    material_name: str = "FUEL",
    leftovers: DefaultDict[str, int] = defaultdict(lambda: 0)
) -> int:
    if material_name == "ORE":
        return req_quantity
    else:
        required_ore = 0
        mat = materials[material_name]

        quantity_to_produce = req_quantity - leftovers[material_name]
        if quantity_to_produce <= 0:
            leftovers[material_name] -= req_quantity
            return 0

        min_batches = (quantity_to_produce - 1) // mat.quantity_per_batch + 1
        quantity_produced = min_batches * mat.quantity_per_batch
        leftover_quantity = (leftovers[material_name] + quantity_produced -
                             req_quantity)
        leftovers[material_name] = leftover_quantity
        for m in mat.recipe:
            ore = dfs(min_batches * int(m[0]), m[1], leftovers)
            required_ore += ore
        return required_ore


parse_input(input_txt)
ore_per_fuel = dfs()
print(ore_per_fuel)

available_ore = 1000000000000
leftovers = defaultdict(lambda: 0)


def dichotomy(req_fuel: int,
              jump_size: int,
              last_operation=None,
              shrink_steps=False) -> int:

    necessary_ore = dfs(req_fuel, "FUEL", leftovers)
    if necessary_ore == available_ore:
        return req_fuel

    # If the jump size is 1, it means we are at the best possible integer
    # value, or just 1 above it.
    if jump_size == 1:
        return req_fuel - 1 * (necessary_ore > available_ore)

    if necessary_ore > available_ore:
        # we check if last_operation is different from the current one
        # because in that case it means we have passed the right value
        # and must start going back down with smaller steps
        if shrink_steps or last_operation == "up":
            jump_size = math.ceil(jump_size / 2)
            shrink_steps = True
        # if we still haven't changed of operation, we keep increasing the jump size
        else:
            jump_size *= 2
        last_operation = "down"
        new_value = req_fuel - jump_size

    elif necessary_ore < available_ore:
        if shrink_steps or last_operation == "down":
            jump_size = math.ceil(jump_size / 2)
            shrink_steps = True
        else:
            jump_size *= 2
        last_operation = "up"
        new_value = req_fuel + jump_size

    return dichotomy(new_value, jump_size, last_operation, shrink_steps)


max_fuel = dichotomy(50000, 25000)
print(max_fuel)
