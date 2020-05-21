import numpy as np

from codebook import CodebookFactory
from pixel_map import PixelMap
from tga import get_closest_vector


DEFAULT_PERTURBATION_VECTOR = int('0b00000001', 2)
DEFAULT_BLOCK_SIDE = 2
DEFAULT_EPSILON = 0.001


class VectorQuantization:
    """
        Class implementing vector quantization of pictures.
    """

    def __init__(self, pixel_table, color_number_exp, block_side=DEFAULT_BLOCK_SIDE):
        self.original_pixel_table = pixel_table
        self.color_number_exp = color_number_exp
        self.block_side = block_side


    def perform(self):
        codebook_factory = CodebookFactory(
            self.original_pixel_table,
            DEFAULT_PERTURBATION_VECTOR,
            self.block_side,
            DEFAULT_EPSILON
        )
        codebook = codebook_factory.create_codebook(self.color_number_exp)
        return self.reconstruct_pixel_table(codebook)


    def reconstruct_pixel_table(self, codebook):
        height = len(self.original_pixel_table.pixels)
        if height == 0:
            return []
        width = len(self.original_pixel_table.pixels[0])
        new_pixel_table = PixelMap(height, width)

        for row_idx in range(0, height, self.block_side):
            for col_idx in range(0, width, self.block_side):
                block = [
                    (pixel.red, pixel.green, pixel.blue) for pixel in np.ndarray.flatten(
                        self.original_pixel_table[row_idx:row_idx+self.block_side, col_idx:col_idx+self.block_side])
                ]
                _, min_idx = get_closest_vector(block, codebook)
                i = 0
                for row_i in range(row_idx, row_idx+self.block_side):
                    for col_i in range(col_idx, col_idx+self.block_side):
                        pixel = codebook[min_idx][i]
                        new_pixel_table.new_pixel(row_i, col_i, pixel[0], pixel[1], pixel[2])
                        i += 1
        return new_pixel_table

