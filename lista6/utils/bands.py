from dataclasses import dataclass
import numpy as np
from utils.pixels import Pixel, PixelDifference, PixelMap, get_pixel
from utils.quantization import Quantization, assign_quantizers_indexes, best_fit_idx



def get_low_band(current, previous):
    return Pixel(
        mean_uint8(current.red, previous.red),
        mean_uint8(current.green, previous.green),
        mean_uint8(current.blue, previous.blue)
    )


def get_high_band(current, previous):
    return PixelDifference(
        deviation(current.red, previous.red),
        deviation(current.green, previous.green),
        deviation(current.blue, previous.blue)
    )


def mean_uint8(current, previous):
    return np.uint8(((np.int(current) + np.int(previous)) // 2) % 256)


def deviation(current, previous):
    return (current - previous) // 2


def split_bands(pixel_map):
    bands = np.empty(pixel_map.size // 2, dtype=BandSplit)
    pixel_input = pixel_map.pixels.flatten()

    for i in range(0, bands.size):
        bands[i] = BandSplit(
            low=get_low_band(pixel_input[i * 2 + 1], pixel_input[i * 2]),
            high=get_high_band(pixel_input[i * 2 + 1], pixel_input[i * 2])
        )
    return bands


@dataclass
class BandSplit:
    low: Pixel
    high: PixelDifference


'''
    Bands encoder/decoder
'''
class BandEncoder:
    def __init__(self, pixel_table, quantizer_bits):
        self.pixel_table = pixel_table
        self.low_quantizer = None
        self.high_quantizer = None
        self.low_encoded_sequence = None
        self.high_encoded_sequence = None
        self.quantizer_bits = quantizer_bits
        self.quantizer_size = 1 << quantizer_bits
        self.height, self.width = pixel_table.pixels.shape

    def encode(self):
        bands = split_bands(self.pixel_table)
        self.encode_high_band(bands)
        self.encode_low_band(bands)

    def encode_high_band(self, bands):
        high_bands = np.array([band.high for band in bands], dtype=BandSplit)
        high_quantization = Quantization(high_bands)
        self.high_quantizer = high_quantization.create_nonuniform_quantizer(self.quantizer_size)
        self.high_encoded_sequence = assign_quantizers_indexes(self.high_quantizer, high_bands)

    def encode_low_band(self, bands):
        low_bands = np.array([band.low for band in bands], dtype=BandSplit)
        self.low_quantizer, self.low_encoded_sequence = self.diff_encode(low_bands)


    def diff_encode(self, original_sequence):
        data_size = original_sequence.size
        data_type = type(original_sequence[0])

        initial_differential_sequence =\
            np.array([
                original_sequence[0]]
                + 
                [
                    original_sequence[i] - original_sequence[i-1]
                    for i in range(1, len(original_sequence))
            ])

        quantization = Quantization(initial_differential_sequence)
        quantizer = quantization.create_nonuniform_quantizer(self.quantizer_size)
        differential_sequence = np.empty(data_size, dtype=data_type)
        differential_sequence[0] = original_sequence[0]
        quantized_idx_sequence = np.empty(data_size, dtype=np.uint8)
        quantized_idx_sequence[0] = best_fit_idx(quantizer, differential_sequence[0])
        encoded_sequence = np.empty(data_size, dtype=data_type)
        encoded_sequence[0] = quantizer[quantized_idx_sequence[0]]

        for i in range(1, data_size):
            differential_sequence[i] = original_sequence[i] - encoded_sequence[i - 1]
            quantized_idx_sequence[i] = best_fit_idx(quantizer, differential_sequence[i])
            encoded_sequence[i] = encoded_sequence[i - 1] + quantizer[quantized_idx_sequence[i]]

        return quantizer, quantized_idx_sequence



class BandDecoder:
    def __init__(self, high_quantizer, low_quantizer):
        self.high_quantizer = high_quantizer
        self.low_quantizer = low_quantizer
        self.decoded_sequence = None
        assert high_quantizer.dtype == low_quantizer.dtype


    def decode(self, high_idx_sequence, low_idx_sequence):
        assert high_idx_sequence.size == low_idx_sequence.size
        decoded_high_sequence = np.array([self.high_quantizer[idx] for idx in high_idx_sequence])
        decoded_low_sequence = self.diff_decode(low_idx_sequence)

        self.decoded_sequence = np.empty(low_idx_sequence.size*2, dtype=self.low_quantizer.dtype)
        for i in range(0, decoded_low_sequence.size):
            self.decoded_sequence[i * 2] = get_pixel(decoded_low_sequence[i] - decoded_high_sequence[i])
            self.decoded_sequence[i * 2 + 1] = decoded_low_sequence[i] + decoded_high_sequence[i]


    def diff_decode(self, idx_sequence):
        quantizer = self.low_quantizer
        decoded_sequence = np.empty(idx_sequence.shape, dtype=quantizer.dtype)
        decoded_sequence[0] = get_pixel(quantizer[idx_sequence[0]])

        for i in range(1, idx_sequence.size):
            decoded_sequence[i] = get_pixel(decoded_sequence[i - 1] + quantizer[idx_sequence[i]])

        return decoded_sequence