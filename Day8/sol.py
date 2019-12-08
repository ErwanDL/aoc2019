import os
import numpy as np
from typing import Tuple
dirname = os.path.dirname(__file__)
input_txt = open(dirname + "/input.txt", "r").read()


class Layer:
    def __init__(self, dimensions: Tuple[int, int]):
        self.dimensions = dimensions
        self.rows = np.zeros(dimensions, dtype=int)

    def __repr__(self):
        return "Layer(" + str(self.rows) + ")"

    def add_pixel(self, flattened_index: int, value: int):
        row = flattened_index // self.dimensions[1]
        col = flattened_index % self.dimensions[1]
        self.rows[row, col] = value

    def pixel_value_counts(self):
        result = {0: 0, 1: 0, 2: 0}
        unique, counts = np.unique(self.rows, return_counts=True)
        result.update(dict(zip(unique, counts)))
        return result


layers = []
data = input_txt[:]
nb_digits = len(data)
dimensions = (6, 25)  # (nb_rows, nb_cols)
nb_pixels = dimensions[0] * dimensions[1]

for i in range(nb_digits // nb_pixels):
    l = Layer(dimensions)
    for j in range(nb_pixels):
        l.add_pixel(j, data[i * nb_pixels + j])
    layers.append(l)

pixel_value_counts = list(map(Layer.pixel_value_counts, layers))
fewer_zeros_layer = min(pixel_value_counts, key=lambda x: x[0])
print(fewer_zeros_layer[1] * fewer_zeros_layer[2])
