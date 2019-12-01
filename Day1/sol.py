from math import floor
import os
dirname = os.path.dirname(__file__)

input_file = open(dirname + "/input.txt", "r").read()

input_list = list(map(int, input_file.split("\n")[:-1]))


def fuel_requirement(mass):
    fuel = floor(mass / 3) - 2
    if fuel <= 0:
        return 0
    else:
        return fuel + fuel_requirement(fuel)


print(fuel_requirement(14), fuel_requirement(1969), fuel_requirement(100756))

result = 0
for module in input_list:
    result += fuel_requirement(module)

print(result)