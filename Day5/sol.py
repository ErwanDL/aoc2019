import os
dirname = os.path.dirname(__file__)

input_txt = open(dirname + "/input.txt", "r").read()

input_list = list(map(int, input_txt.split(",")))

data = input_list[:]


def get_digit_right_to_left(number, digit_position):
    """
        Extracts from the input number the digit at the given position 
        from right to left, starting at 0.
    """
    if digit_position <= 0:
        return number % 10
    else:
        return get_digit_right_to_left(number // 10, digit_position - 1)


# Every operation returns an instruction pointer value


def op_sum(instruction_index, i_first_value, i_second_value, i_store_result):
    data[i_store_result] = data[i_first_value] + data[i_second_value]
    return instruction_index + 4


def op_multiply(instruction_index, i_first_value, i_second_value,
                i_store_result):
    data[i_store_result] = data[i_first_value] * data[i_second_value]
    return instruction_index + 4


def op_input(instruction_index, i_store_input):
    value = input("Enter the desired value : ")
    data[i_store_input] = int(value)
    return instruction_index + 2


def op_output(instruction_index, i_value):
    print(data[i_value])
    return instruction_index + 2


def op_jump_if_true(instruction_index, i_first_value, i_second_value):
    if data[i_first_value] != 0:
        return data[i_second_value]
    else:
        return instruction_index + 3


def op_jump_if_false(instruction_index, i_first_value, i_second_value):
    if data[i_first_value] == 0:
        return data[i_second_value]
    else:
        return instruction_index + 3


def op_less_than(instruction_index, i_first_value, i_second_value,
                 i_store_result):
    if data[i_first_value] < data[i_second_value]:
        data[i_store_result] = 1
    else:
        data[i_store_result] = 0
    return instruction_index + 4


def op_equal_to(instruction_index, i_first_value, i_second_value,
                i_store_result):
    if data[i_first_value] == data[i_second_value]:
        data[i_store_result] = 1
    else:
        data[i_store_result] = 0
    return instruction_index + 4


def apply_mode_to_param(modes, instruction_index, param_nb):
    """
        Applies the corresponding mode to the input param_nb based on the
        "modes" of the associated instruction.
        Returns an index (the parameter's index if
        immediate mode, or its value if position mode).
    """
    mode = get_digit_right_to_left(modes, param_nb - 1)
    if mode == 1:
        return instruction_index + param_nb
    else:
        return data[instruction_index + param_nb]


def parse_instruction(index):
    """
        Parses an instruction, executes it with the correct mode and returns
        the index of the next instruction or -1 if terminated.
    """
    instruction = data[index]
    opcode = instruction % 100

    if opcode == 99:
        return -1

    modes = instruction // 100

    def param(param_nb):
        return apply_mode_to_param(modes, index, param_nb)

    if opcode == 1:
        return op_sum(index, param(1), param(2), param(3))
    if opcode == 2:
        return op_multiply(index, param(1), param(2), param(3))
    if opcode == 3:
        return op_input(index, param(1))
    if opcode == 4:
        return op_output(index, param(1))
    if opcode == 5:
        return op_jump_if_true(index, param(1), param(2))
    if opcode == 6:
        return op_jump_if_false(index, param(1), param(2))
    if opcode == 7:
        return op_less_than(index, param(1), param(2), param(3))
    if opcode == 8:
        return op_equal_to(index, param(1), param(2), param(3))


def run_program():
    index = 0
    while index != -1:
        index = parse_instruction(index)


run_program()
