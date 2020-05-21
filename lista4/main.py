import argparse
import math
from tga_reader import TGAReader
from predictors import *


def parse_arguments():
    arg_parser = argparse.ArgumentParser('TGA to JPEGLS enthropy counter.')
    arg_parser.add_argument('input_file', help='TGA file.' )
    return arg_parser.parse_args()


def print_results(color, red, green, blue):
    print('File:', color, '\tR:', red, '\tG:', green, '\tB:', blue, '\n')


def print_entropies(entropy):
    print_results(entropy.get_color(), entropy.get_red(), entropy.get_green(), entropy.get_blue())
    

def calculate_predictors(original_pixel_map):
    entropies = {}
    entropies['W'] = PredictorW(original_pixel_map).codes.entropy
    entropies['N'] = PredictorN(original_pixel_map).codes.entropy
    entropies['NW'] = PredictorNW(original_pixel_map).codes.entropy
    entropies['N+W-NW'] = PredictorNAddWSubNW(original_pixel_map).codes.entropy
    entropies['N+(W-NW)/2'] = PredictorNAddHalfWSubNW(original_pixel_map).codes.entropy
    entropies['W+(N-NW)/2'] = PredictorWAddHalfNSubNW(original_pixel_map).codes.entropy
    entropies['(N+W)/2'] = PredictorHalfNAddW(original_pixel_map).codes.entropy
    entropies['NEW'] = PredictorNew(original_pixel_map).codes.entropy
    return entropies
            

def encode(pixel_map):
    entropies = calculate_predictors(pixel_map)
    entropies['ORIGINAL'] = pixel_map.entropy

    min_color = ('ORIGINAL', pixel_map.entropy.get_color())
    min_red = ('ORIGINAL', pixel_map.entropy.get_red())
    min_green = ('ORIGINAL', pixel_map.entropy.get_green())
    min_blue = ('ORIGINAL', pixel_map.entropy.get_blue())

    for key, entropy in entropies.items():
        
        if key == 'ORIGINAL':
            print('#################################################################################################\n')

        print(key)
        print_entropies(entropy)

        if entropy.get_color() < min_color[1]:
            min_color = (key, entropy.get_color())
        if entropy.get_red() < min_red[1]:
            min_red = (key, entropy.get_red())
        if entropy.get_green() < min_green[1]:
            min_green = (key, entropy.get_green())
        if entropy.get_blue() < min_blue[1]:
            min_blue = (key, entropy.get_blue())

    print('BEST')
    print('File:\t', min_color[1], '\t', min_color[0],
        '\nR:\t', min_red[1], '\t', min_red[0],
        '\nG:\t', min_green[1], '\t', min_green[0],
        '\nB:\t', min_blue[1], '\t', min_blue[0],
        '\n')


def main():
    args = parse_arguments()
    print(args.input_file, '\n')
    tga_reader = TGAReader(args.input_file)
    encode(tga_reader.pixel_map)


if __name__ == "__main__":
    main()