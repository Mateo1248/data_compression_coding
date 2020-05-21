"""Program to compress with LZW algorithm."""
import argparse
import contextlib

import encoding
import decoding
from inout_bits import *
from lzw import *



def parse_arguments(argparser):
    argparser.add_argument("-encode", metavar=("input", "output"), nargs=2, help='Zakoduj plik wejściowy, wynik zapisz w wyjściowym.')

    argparser.add_argument("-decode", metavar=("input", "output"), nargs=2, help='Odkoduj plik wejściowy, wynik zapisz w wyjściowym.')

    argparser.add_argument('-type', choices=['gamma', 'delta', 'omega', 'fib'], default='omega',help='Wybór kodowania pliku (domyślnie omega)')

    return argparser.parse_args()


def get_coding(module, arg):
    if arg == 'gamma':
        return module.Gamma
    if arg == 'delta':
        return module.Delta
    if arg == 'fib':
        return module.Fibonacci
    return module.Omega


def main():
    argparser = argparse.ArgumentParser(description='LZW')
    args = parse_arguments(argparser)

    if args.encode:
        with open(args.encode[0], 'rb') as input_file, contextlib.closing(BitOutputStream(open(args.encode[1], "wb"))) as bit_out:
            dictionary = dict([(bytes((x,)), x) for x in range(256)])
            dictionary[None] = 256
            dict_set = set(dictionary.keys())
            enc = LZWEncoder(dictionary, input_file, get_coding(encoding, args.type)(bit_out), dict_set)
            enc.encode()
            print('Typ kodowania:', args.type)
            print('Rozmiar pliku wejściowego:', enc.get_totalbytes(), 'b')
            print('Rozmiar po komresji:', bit_out.get_totalbytes(), 'b')
            print('Współczynnik kompresji:', enc.get_totalbytes()/bit_out.get_totalbytes())
            print('Entropia pliku wejściowego:', enc.get_input_entropy())
            print('Entropia po kompresji:', bit_out.get_output_entropy())
    
    elif args.decode:
        with open(args.decode[1], 'wb') as output_file, contextlib.closing(BitInputStream(open(args.decode[0], "rb"))) as input:
            dictionary = [bytes((x,)) for x in range(256)]
            dictionary.append(None)  # EOF
            dec = LZWDecoder(dictionary, output_file, get_coding(decoding, args.type)(input))
            dec.decode()
    else:
        argparser.parse_args(["--help"])


if __name__ == '__main__':
    main()
