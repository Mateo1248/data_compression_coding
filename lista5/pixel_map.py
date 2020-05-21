import numpy as np
from dataclasses import dataclass


@dataclass
class Pixel:
    """
        Data class representing single pixel of the image.
        Pixel consist of three RGB colors.
    """
    red: np.uint8
    green: np.uint8
    blue: np.uint8


    @property
    def color(self):
        return (self.red << 16) + (self.green << 8) + self.blue


class PixelMap:
    """
        Map wrapper of the image pixels.
        Pixel Map stores pixels of the image.
    """
    def __init__(self, height, width):
        self.width = width
        self.height = height
        self.pixels = np.empty((height, width), dtype=Pixel)


    def __getitem__(self, idx):
        row, col = idx
        return self.pixels[row, col]


    def new_pixel(self, row, col, red, blue, green):
        assert row < self.height and col < self.width, f"Out of range: [{row}, {col}]"
        pixel = Pixel(red % 256, blue % 256, green % 256)
        self.pixels[row, col] = pixel
        

    @property
    def size(self):
        return self.height * self.width


    def __str__(self):
        return str(self.pixels)


    def get_blocks(self, block_side):
        blocks = []
        for row_idx in range(0, self.height, block_side):
            for col_idx in range(0, self.width, block_side):
                blocks.append([(pixel.red, pixel.green, pixel.blue) for pixel in np.ndarray.flatten(self.pixels[row_idx:row_idx+block_side, col_idx:col_idx+block_side])])
        return np.array(blocks, dtype=np.uint8)
