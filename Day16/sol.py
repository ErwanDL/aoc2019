import os
dirname = os.path.dirname(__file__)
input_txt = open(dirname + "/input.txt", "r").read()
input_list = list(map(int, list(input_txt)))


class Signal:
    def __init__(self, input_signal: List[int]):
        self.signal = input_signal[:]
        self.pattern = [0, 1, 0, -1]
        self.cursor = 1

    def apply_FFT(self) -> None:
        for i, digit in enumerate(self.signal):
            pattern_index = i // self.cursor
        self.cursor += 1