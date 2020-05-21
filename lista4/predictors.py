from tga_reader import PixelMap
from abc import ABC, abstractmethod


"""
-- N
-- W
-- NW
-- N + W - NW
-- N + (W - NW)/2
-- W + (N - NW)/2
-- (N + W)/2
-- New standard
"""


get_red = lambda color : color.red
get_green = lambda color : color.green
get_blue = lambda color : color.blue


class Predictor(ABC):
    """Abstract class for prediction calculation of the whole pixel map."""

    def __init__(self, pixel_map):
        self.original_pixel_map = pixel_map
        self.codes = PixelMap(pixel_map.height, pixel_map.width)
        self.build_codes()


    def build_codes(self):
        for row in range(self.codes.height):
            for col in range(self.codes.width):
                self.codes.new_pixel(
                    row, col, 
                    self._get_prediction(row, col, get_red),
                    self._get_prediction(row, col, get_green),
                    self._get_prediction(row, col, get_blue)
                )

    def _get_prediction(self, row, column, color_extractor):
        n = color_extractor(self.n(row, column))
        w = color_extractor(self.w(row, column))
        nw = color_extractor(self.nw(row, column))
        return color_extractor(self.original_pixel_map[row, column]) - self.get_prediction(n, w, nw)


    @abstractmethod
    def get_prediction(self, n, w, nw):
        pass


    def n(self, row, col):
        return self.original_pixel_map[row-1, col]


    def w(self, row, col):
        return self.original_pixel_map[row, col-1]


    def nw(self, row, col):
        return self.original_pixel_map[row-1, col-1]


class PredictorN(Predictor):
    def get_prediction(self, n, w, nw):
        return n


class PredictorW(Predictor):
    def get_prediction(self, n, w, nw):
        return w


class PredictorNW(Predictor):
    def get_prediction(self, n, w, nw):
        return nw


class PredictorNAddWSubNW(Predictor):
    def get_prediction(self, n, w, nw):
        return n + w - nw


class PredictorNAddHalfWSubNW(Predictor):
    def get_prediction(self, n, w, nw):
        return n + (w - nw)//2


class PredictorWAddHalfNSubNW(Predictor):
    def get_prediction(self, n, w, nw):
        return w + (n - nw)//2


class PredictorHalfNAddW(Predictor):
    def get_prediction(self, n, w, nw):
        return (w + n)//2

class PredictorNew(Predictor):
    def get_prediction(self, n, w, nw):
        m = max(w, n)
        if nw >= m:
            return m
        m = min(w, n)
        if nw <= m:
            return m
        return w + n - nw