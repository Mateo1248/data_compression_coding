from utils.inout import *
import argparse
import random


def check(in1: BitInputStream, in2: BitOutputStream):
    
    counter = 0

    try: 
        while True:
            b1 = in1.bit_array(4)
            b2 = in2.bit_array(4)
            
            if not (b1 == b2).all():
                print(b1, b2)
                counter += 1

    except:
        close_stream(in1, in2)

    print(f"Mismatched blocks: {counter}")

def main():
    parser = argparse.ArgumentParser(description="Program compares each 4 bits blocks in files.")
    parser.add_argument("file1")
    parser.add_argument("file2")
    args = parser.parse_args()


    check(
        *open_inin(args.file1, args.file2)
    )

if __name__ == "__main__":
    main()