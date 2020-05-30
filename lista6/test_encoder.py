import argparse
from utils.tga import TGAReader, write_tga_pixel_vector
from utils.bands import BandEncoder, BandDecoder
from utils.inout import CompressFileWriter, CompressFileReader



def main():
    arg_parser = argparse.ArgumentParser(description='TGA encoder')
    arg_parser.add_argument('input_file')
    arg_parser.add_argument('output_file')
    arg_parser.add_argument('quantizer_bits',help='Number of quantizer bits',type=int,choices=[1, 2, 3, 4, 5, 6, 7])
    args = arg_parser.parse_args()

    tga_reader = TGAReader(args.input_file)
    encoder = BandEncoder(tga_reader.pixel_map, args.quantizer_bits)
    encoder.encode()

    file_writer = CompressFileWriter(
        args.output_file,
        tga_reader.header['height'],
        tga_reader.header['width'],
        args.quantizer_bits
    )

    file_writer.write(
        encoder.high_quantizer,
        encoder.high_encoded_sequence,
        encoder.low_quantizer,
        encoder.low_encoded_sequence
    )


if __name__ == "__main__":
    main()