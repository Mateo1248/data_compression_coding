import argparse

from tga import TGAReader, write_tga
from vector_quantization import VectorQuantization
from distortion import DistortionCalculator


def parse_arguments():
    arg_parser = argparse.ArgumentParser(description='TGA quantization.')
    arg_parser.add_argument('input_file',help='Input TGA file.')
    arg_parser.add_argument('output_file',help='Output compressed file.')
    arg_parser.add_argument('color_number_exp',help='Number which binary power will be number of colors.',type=int)

    return arg_parser.parse_args()


def print_distortions(original_pixel_table, reconstructed_pixel_table):
    dc = DistortionCalculator(original_pixel_table, reconstructed_pixel_table)
    mse = dc.mse()
    print('Mean square error:', mse)
    snr = dc.snr(mse=mse)
    print('Signal to noise ratio:', snr)
    snr_db = dc.snr_db(snr=snr)
    print('Signal to noise ratio (decibels):', snr_db)


def main():
    args = parse_arguments()
    tga_reader = TGAReader(args.input_file)
    vq = VectorQuantization(tga_reader.pixel_map, args.color_number_exp)
    reconstructed_pixel_table = vq.perform()

    write_tga(
        args.output_file, 
        tga_reader.header, 
        reconstructed_pixel_table, 
        tga_reader.footer
    )

    print_distortions(tga_reader.pixel_map, reconstructed_pixel_table)


if __name__ == "__main__":
    main()
