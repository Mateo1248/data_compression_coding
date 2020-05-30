import argparse
from utils.tga import TGAReader
from utils.distortion import DistortionCalculator



def print_distortions(original_pixel_table, reconstructed_pixel_table):
    dc = DistortionCalculator(original_pixel_table, reconstructed_pixel_table)
    mse = dc.mse()
    print('Mean square error (MSE):', mse)
    snr = dc.snr(mse=mse)
    print('Signal to noise ratio:', snr)
    snr_db = dc.snr_db(snr=snr)
    print('Signal to noise ratio (decibels):', snr_db)

    print('\nRed MSE:', dc.red_mse())
    print('Green MSE:', dc.green_mse())
    print('Blue MSE:', dc.blue_mse())


def main():
    arg_parser = argparse.ArgumentParser(description='TGA orginal/decoded file compare.')
    arg_parser.add_argument('original')
    arg_parser.add_argument('decoded')
    args = arg_parser.parse_args()

    original = TGAReader(args.original)
    reconstructed = TGAReader(args.decoded)
    print_distortions(original.pixel_map, reconstructed.pixel_map)


if __name__ == "__main__":
    main()