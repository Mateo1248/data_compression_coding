import math


def squared_difference(original, quantized):
    return (int(original) - int(quantized))**2


def unit_error(original_pixel, quantized_pixel):
    return (squared_difference(original_pixel.red, quantized_pixel.red)
            + squared_difference(original_pixel.green, quantized_pixel.green)
            + squared_difference(original_pixel.blue, quantized_pixel.blue))


def red_error(original, reconstructed):
    return squared_difference(original.red, reconstructed.red)


def green_error(original, reconstructed):
    return squared_difference(original.green, reconstructed.green)


def blue_error(original, reconstructed):
    return squared_difference(original.blue, reconstructed.blue)


class DistortionCalculator:
    """
        Calculator of distortions values:
        MSE -- Mean Square Error
        SNR -- Signal to Noise Ratio
    """

    def __init__(self, original, reconstructed):
        self.original = original
        self.reconstructed = reconstructed
        self.height = len(self.original.pixels)
        if self.height > 0:
            self.width = len(self.original.pixels[0])
        else:
            self.width = 0

    def mse(self):
        return self._mse(unit_error)/3

    def red_mse(self):
        return self._mse(red_error)

    def green_mse(self):
        return self._mse(green_error)

    def blue_mse(self):
        return self._mse(blue_error)

    def _mse(self, error_fn):
        s = 0
        for row in range(self.height):
            for col in range(self.width):
                o = self.original[row, col]
                r = self.reconstructed[row, col]
                s += error_fn(o, r)
        return s/(self.height*self.width)


    def snr(self, mse=None):
        if mse:
            s = 0
            for row in self.original.pixels:
                for pixel in row:
                    s += pixel.red**2
                    s += pixel.green**2
                    s += pixel.blue**2
            if mse == 0:
                return float('inf')
            return (s/(3*self.height*self.width))/mse
        else:
            s = 0
            for row in self.original.pixels:
                for pixel in row:
                    s += pixel.red**2
                    s += pixel.green**2
                    s += pixel.blue**2
            mse = self.mse()
            if mse == 0:
                return float('inf')
            return (s/(3*self.height*self.width))/mse


    def snr_db(self, snr=None):
        if snr:
            return 10*math.log10(snr)
        else:
            return 10*math.log10(self.snr())
