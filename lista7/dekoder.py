from utils.hamming import *
import argparse


def main():
    parser = argparse.ArgumentParser(description="Extended hamming decoder.")
    parser.add_argument("input", help="Encoded input file.")
    parser.add_argument("output", help="File to write decoded result.")
    args = parser.parse_args()

    hm = Hamming()
    hm.decode(args.input, args.output)


if __name__ == "__main__":
    main()