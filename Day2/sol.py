import os
dirname = os.path.dirname(__file__)

input_file = open(dirname + "/input.txt", "r").read()

input_list = list(map(int, input_file.split(",")))


def initialize_program(noun, verb):
    data = input_list[:]
    data[1] = noun
    data[2] = verb
    return data


def parse_opcode(data, index):
    i0 = data[index]
    if i0 == 99:
        return

    i1 = data[index + 1]
    i2 = data[index + 2]
    i3 = data[index + 3]
    if i0 == 1:
        s = data[i1] + data[i2]
        data[i3] = s
    elif i0 == 2:
        p = data[i1] * data[i2]
        data[i3] = p
    parse_opcode(data, index + 4)


def run_program(data):
    parse_opcode(data, 0)
    return data[0]


for i in range(100):
    for j in range(100):
        output = run_program(initialize_program(i, j))
        if output == 19690720:
            print(i, j, 100 * i + j)
            break