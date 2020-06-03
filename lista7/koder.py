from utils.hamming import *
import argparse


def main():
    parser = argparse.ArgumentParser(description="Extended hamming encoder.")
    parser.add_argument("input", help="File to encode.")
    parser.add_argument("output", help="File to write encoded result.")
    args = parser.parse_args()

    hm = Hamming()
    hm.encode(args.input, args.output)


if __name__ == "__main__":
    main()

