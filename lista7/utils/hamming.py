import numpy as np
from utils.inout import *


class Hamming:
    '''
        Hamming SECDED coder/encoder.
    '''

    generator: np.array
    parity_check: np.array
    input: BitInputStream
    output: BitOutputStream

    def __init__(self):
        super().__init__()
        self.generator = np.array(
            [
                [1,0,0,0],
                [0,1,0,0],
                [0,0,1,0],
                [0,0,0,1],

                [0,1,1,1],
                [1,0,1,1],
                [1,1,0,1],
                [1,1,1,1]
            ],
            dtype=np.uint8
        )
        

    def encode(self, input_file, output_file):
        bit_in, bit_out = open_inout(input_file, output_file)

        try:
            while True:
                data = bit_in.bit_array(4)
                encoded = np.dot(self.generator, data)%2
                
                for b in encoded.astype(int):
                    bit_out.write_bit(b)

        except Exception as e:
            close_stream(bit_in, bit_out)
            

    def decode(self, input_file, output_file):
        bit_in, bit_out = open_inout(input_file, output_file)

        try:
            single_err = 0
            double_err = 0
            while True:
                encoded = bit_in.bit_array(8)
                wrong_bit = int(
                    ((encoded[3] + encoded[4] + encoded[5] + encoded[6]) % 2) * 4 + \
                    ((encoded[1] + encoded[2] + encoded[5] + encoded[6]) % 2) * 2 + \
                    ((encoded[0] + encoded[2] + encoded[4] + encoded[6]) % 2)
                )
                parity = int(
                    np.sum(encoded[:7])%2
                )
            
                if wrong_bit > 0:
                    if parity == 0:
                        double_err += 1
                    else:
                        single_err += 1
                        if wrong_bit < 4:
                            encoded[wrong_bit-1] = (encoded[wrong_bit-1]+1)%2 


                for b in encoded[:4].astype(int):
                    bit_out.write_bit(b)
        except:
            close_stream(bit_in, bit_out)
        

        print(f"Single error counter: {single_err}")
        print(f"Double error counter: {double_err}")
        
