from utils.inout import *
import argparse
import random


def noise(bit_in: BitInputStream, bit_out: BitOutputStream, p: float):
    
    while True:
        bit = bit_in.read_bit()
        if bit < 0:
            close_stream(bit_in, bit_out)
            break

        if random.random() < p:
            bit = (bit+1)%2

        bit_out.write_bit(bit)


def main():
    parser = argparse.ArgumentParser(description="Program spares each bit from input with probability p and save result to output.")
    parser.add_argument("input", help="Input file.")
    parser.add_argument("output", help="Output file.")
    parser.add_argument("p", help="Probability.", type=float)
    args = parser.parse_args()


    noise(
        *open_inout(args.input, args.output),
        args.p
    )

if __name__ == "__main__":
    main()