import os
dirname = os.path.dirname(__file__)
input_txt = open(dirname + "/input.txt", "r").read()
input_list = list(map(int, input_txt.split(",")))

from typing import List
import numpy as np
from intcode_computer import IntcodeComputer, EndOfProgram

area_side = 50
affected = 0
input_instructions = []


def is_affected_at(x: int, y: int) -> int:
    return IntcodeComputer(input_list, [x, y]).run_to_next_output()


for x in range(area_side):
    for y in range(area_side):
        affected += is_affected_at(x, y)
print(affected)

startY = 100
startX = 0
res = None
while True:
    while not is_affected_at(startX, startY):
        startX += 1
    if is_affected_at(startX + 99, startY - 99):
        res = (startX, startY - 99)
        break
    startY += 1
print(res, res[0] * 10000 + res[1])
