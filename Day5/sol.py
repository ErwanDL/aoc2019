import os
dirname = os.path.dirname(__file__)
input_txt = open(dirname + "/input.txt", "r").read()
input_list = list(map(int, input_txt.split(",")))


def get_digit_right_to_left(number, digit_position):
    """
        Extracts from the input number the digit at the given position 
        from right to left, starting at 0.
    """
    if digit_position <= 0:
        return number % 10
    else:
        return get_digit_right_to_left(number // 10, digit_position - 1)


class IntcodeParser():
    def __init__(self, data):
        self.data = data
        self.pointer = 0
        self.modes = 0

    def param(self, param_nb):
        """
            Applies the appropriate mode to the param at self.pointer + param_nb
            and returns the resulting value.
        """
        mode = get_digit_right_to_left(self.modes, param_nb - 1)
        param_index = self.pointer + param_nb
        return self.data[param_index] if mode == 1 else self.data[
            self.data[param_index]]

    def op_sum(self):
        storage_index = self.data[self.pointer + 3]
        self.data[storage_index] = self.param(1) + self.param(2)
        self.pointer += 4

    def op_multiply(self):
        storage_index = self.data[self.pointer + 3]
        self.data[storage_index] = self.param(1) * self.param(2)
        self.pointer += 4

    def op_input(self):
        value = input("Enter the desired value : ")
        storage_index = self.data[self.pointer + 1]
        self.data[storage_index] = int(value)
        self.pointer += 2

    def op_output(self):
        print(self.param(1))
        self.pointer += 2

    def op_jump_if_true(self):
        self.pointer = self.param(2) if (
            self.param(1) != 0) else self.pointer + 3

    def op_jump_if_false(self):
        self.pointer = self.param(2) if (
            self.param(1) == 0) else self.pointer + 3

    def op_less_than(self):
        storage_index = self.data[self.pointer + 3]
        self.data[storage_index] = 1 if (self.param(1) < self.param(2)) else 0
        self.pointer += 4

    def op_equal_to(self):
        storage_index = self.data[self.pointer + 3]
        self.data[storage_index] = 1 if (self.param(1) == self.param(2)) else 0
        self.pointer += 4

    def parse_next_instruction(self):
        """
            Parses an instruction, executes it with the correct mode and returns
            the index of the next instruction or -1 if terminated.
        """
        instruction = self.data[self.pointer]
        opcode = instruction % 100

        if opcode == 99:
            self.pointer = -1

        self.modes = instruction // 100

        if opcode == 1:
            self.op_sum()
        if opcode == 2:
            self.op_multiply()
        if opcode == 3:
            self.op_input()
        if opcode == 4:
            self.op_output()
        if opcode == 5:
            self.op_jump_if_true()
        if opcode == 6:
            self.op_jump_if_false()
        if opcode == 7:
            self.op_less_than()
        if opcode == 8:
            self.op_equal_to()

    def run(self):
        while self.pointer != -1:
            self.parse_next_instruction()


parser = IntcodeParser(input_list[:])
parser.run()