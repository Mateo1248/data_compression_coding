import argparse
from utils.bands import BandDecoder
from utils.inout import CompressFileReader
from utils.tga import write_tga_pixel_vector, get_default_header, get_default_footer



def main():
    arg_parser = argparse.ArgumentParser(description='TGA decoder')
    arg_parser.add_argument('input_file')
    arg_parser.add_argument('output_file')
    args = arg_parser.parse_args()

    file_reader = CompressFileReader(args.input_file)
    file_reader.read()
    decoder = BandDecoder(file_reader.high_quantizer, file_reader.low_quantizer)
    decoder.decode(file_reader.high_idx_sequence, file_reader.low_idx_sequence)

    write_tga_pixel_vector(
        args.output_file,
        get_default_header(file_reader.width, file_reader.height),
        decoder.decoded_sequence,
        get_default_footer()
    )


if __name__ == "__main__":
    main()