import os
dirname = os.path.dirname(__file__)
input_txt = open(dirname + "/input.txt", "r").read()
input_list = list(map(int, list(input_txt)))
from typing import List

test = list(map(int, list("02935109699940807407585447034323")))


class Signal:
    def __init__(self, input_signal: List[int], repeat=False):
        self.pattern = [0, 1, 0, -1]
        self.repeat = repeat
        if not repeat:
            self.values = input_signal[:]
        else:
            repeated_signal = input_signal[:] * 10000
            self.message_offset = int("".join(
                [str(i) for i in input_signal[:7]]))
            self.values = repeated_signal[self.message_offset:]

    def _FFT_no_repeat(self) -> None:
        new_values = []
        for i in range(len(self.values)):
            new_val = 0
            for j in range(i, len(self.values)):
                pattern_index = ((j + 1) // (i + 1)) % 4
                new_val += self.values[j] * self.pattern[pattern_index]
            new_values.append(abs(new_val) % 10)
        self.values = new_values

    def _FFT_with_repeat(self) -> None:
        new_values = [0] * len(self.values)
        s = 0
        for i in range(len(self.values) - 1, -1, -1):
            s += self.values[i]
            new_values[i] = s % 10
        self.values = new_values

    def FFT(self) -> None:
        self._FFT_with_repeat() if self.repeat else self._FFT_no_repeat()


sig = Signal(input_list, repeat=True)
for i in range(100):
    print(i)
    sig.FFT()
print(sig.values[:8])