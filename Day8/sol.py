import os
import numpy as np
from typing import Tuple, Dict
from collections import defaultdict
dirname = os.path.dirname(__file__)
input_txt = open(dirname + "/input.txt", "r").read()


class Layer:
    def __init__(self, dimensions: Tuple[int, int]):
        self.dimensions = dimensions
        self.pixels = np.zeros(dimensions, dtype=int)

    def __repr__(self):
        return "Layer(" + str(self.pixels) + ")"

    def add_pixel(self, flattened_index: int, value: int) -> None:
        row = flattened_index // self.dimensions[1]
        col = flattened_index % self.dimensions[1]
        self.pixels[row, col] = value

    def pixel_value_counts(self) -> Dict[int, int]:
        unique, counts = np.unique(self.pixels, return_counts=True)
        # defaultdict in case there is not at least 1 of each possible value
        return defaultdict(lambda: 0, zip(unique, counts))


class Image():
    def __init__(self, dimensions: Tuple[int, int], data: str):
        self.dimensions = dimensions
        self.layers: List[Layer] = []

        nb_digits = len(data)
        pixels_per_layer = dimensions[0] * dimensions[1]

        for i in range(nb_digits // pixels_per_layer):
            l = Layer(dimensions)
            for j in range(pixels_per_layer):
                l.add_pixel(j, int(data[i * pixels_per_layer + j]))
            self.layers.append(l)

    # function that returns the solution to part 1
    def part1_solution(self) -> int:
        pixel_value_counts = list(map(Layer.pixel_value_counts, self.layers))
        fewer_zeros_layer_value_counts = min(pixel_value_counts,
                                             key=lambda x: x[0])

        return fewer_zeros_layer_value_counts[
            1] * fewer_zeros_layer_value_counts[2]

    def decode(self) -> Layer:
        final_image = Layer(self.dimensions)
        for row in range(self.dimensions[0]):
            for col in range(self.dimensions[1]):
                for l in self.layers:
                    if l.pixels[row, col] != 2:
                        final_image.pixels[row, col] = l.pixels[row, col]
                        break
        return final_image


img = Image((6, 25), input_txt[:])

print(img.part1_solution())
print(img.decode().pixels)
