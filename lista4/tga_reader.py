import numpy as np
from dataclasses import dataclass
from entropy import ColorEntropy


def extract_header(file):
    header = {}
    header['id-length'] = file.read(1)[0]
    header['color-map-type'] = file.read(1)[0]
    header['image-type'] = file.read(1)[0]
    header['color-map-first-entry-index'] = file.read(1)[0] + (file.read(1)[0] << 8)
    header['color-map-length'] = file.read(1)[0] + (file.read(1)[0] << 8)
    header['color-map-entry-size'] = file.read(1)[0]
    header['x-origin'] = file.read(1)[0] << 8 + file.read(1)[0]
    header['y-origin'] = file.read(1)[0] << 8 + file.read(1)[0]
    header['width'] = file.read(1)[0] + (file.read(1)[0] << 8)
    header['height'] = file.read(1)[0] + (file.read(1)[0] << 8)
    header['pixel-depth'] = file.read(1)[0]
    header['descriptor'] = file.read(1)[0]
    return header


def read_image(file, height, width):
    pixel_map = PixelMap(height, width)
    for row in range(height-1, -1, -1):
        for col in range(width):
            blue = file.read(1)[0]
            green = file.read(1)[0]
            red = file.read(1)[0]
            pixel_map.new_pixel(row, col, red, green, blue)
    
    return pixel_map


class TGAReader:
    """Reader of TGA files."""

    def __init__(self, filename):
        self.filename = filename
        self.header, self.pixel_map = self.read_file()


    def read_file(self):
        with open(self.filename, 'rb') as file:
            header = extract_header(file)
            assert header['id-length'] == header['color-map-length'] == 0, "ID or Color Map length > 0"
            assert header['pixel-depth'] == 24, "Pixel depth != 24 (3 bytes)"
            pixel_map = read_image(file, header['height'], header['width'])
        return header, pixel_map


@dataclass
class Pixel:
    """
        Data class representing single pixel of the image.
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
        Pixel Map stores pixels of the image and calculates entropy of the data.
    """

    def __init__(self, height, width):
        self.width = width
        self.height = height
        self.pixels = np.empty((height, width), dtype=Pixel)
        self.entropy = ColorEntropy()

    def __getitem__(self, idx):
        row, col = idx
        if -1 < row < self.height and -1 < col < self.width:
            return self.pixels[row, col]
        return Pixel(0, 0, 0)

    def new_pixel(self, row, col, red, blue, green):
        assert row < self.height and col < self.width, f"Out of range: [{row}, {col}]"
        pixel = Pixel(red % 256, blue % 256, green % 256)
        self.pixels[row, col] = pixel
        self.entropy.new_value(pixel)
        
    @property
    def size(self):
        return self.height * self.width

    def __str__(self):
        return str(self.pixels)