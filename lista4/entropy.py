import math


def get_red(value):
    return value >> 16


def get_green(value):
    return value >> 8 & 255


def get_blue(value):
    return value & 255


def update_counter(counter, value):
    if value not in counter.keys():
        counter[value] = 1
    else:
        counter[value] += 1


class ColorEntropy:
    """Wrapper of all color entropies: full color, red, green, blue."""

    def __init__(self):
        self.color_entropy = Entropy()
        self.red_entropy = Entropy()
        self.green_entropy = Entropy()
        self.blue_entropy = Entropy()

    def new_value(self, pixel):
        self.color_entropy.new_value(pixel.red)
        self.color_entropy.new_value(pixel.green)
        self.color_entropy.new_value(pixel.blue)
        self.red_entropy.new_value(pixel.red)
        self.green_entropy.new_value(pixel.green)
        self.blue_entropy.new_value(pixel.blue)

    def get_color(self):
        return self.color_entropy.get()

    def get_red(self):
        return self.red_entropy.get()

    def get_green(self):
        return self.green_entropy.get()

    def get_blue(self):
        return self.blue_entropy.get()


class Entropy:
    """Class for calculating entropy."""

    def __init__(self):
        self.total = 0
        self.value_counter = {}

    def new_value(self, value):
        self.total += 1
        update_counter(self.value_counter, value)

    def get(self):
        return sum([x*(math.log(self.total,2)-math.log(x,2)) for x in self.value_counter.values()])/self.total
        