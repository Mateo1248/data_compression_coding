import numpy as np


class BitInputStream:
    """
        Class handling streaming bits from the input.
    """
    def __init__(self, inp):
        self.input = inp
        self.bitbuffer = 0
        self.buffersize = 0


    def read_bit(self):
        if self.bitbuffer == -1:
            return -1
        if self.buffersize == 0:
            temp = self.input.read(1)
            if len(temp) == 0:
                self.bitbuffer = -1
                return -1
            self.bitbuffer = temp[0]
            self.buffersize = 8
        self.buffersize -= 1
        return (self.bitbuffer >> self.buffersize) & 1


    def read_byte(self):
        return self.input.read(1)[0]


    def read_bits(self, number_of_bits):
        value = 0
        for _ in range(number_of_bits):
            value <<= 1
            value += self.read_bit()
        return value

    def bit_array(self, number_of_bits):
        bit_arr = np.zeros((number_of_bits,))
        for i in range(number_of_bits):
            bit_arr[i] = self.read_bit()
            if bit_arr[i] < 0:
                raise EOFError
        return bit_arr


    def close(self):
        self.input.close()
        self.bitbuffer = -1
        self.buffersize = 0



class BitOutputStream:
    """
        Class handling streaming bits to the output.
    """
    def __init__(self, out):
        self.output = out
        self.bitbuffer = 0
        self.buffersize = 0
        self.totalbytes = 0

    def write_bit(self, bit):
        if bit not in (0, 1):
            raise ValueError("Argument must be 0 or 1")
        self.bitbuffer = (self.bitbuffer << 1) | bit
        self.buffersize += 1
        if self.buffersize == 8:
            towrite = bytes((self.bitbuffer,))
            self.output.write(towrite)
            self.totalbytes += 1
            self.bitbuffer = 0
            self.buffersize = 0


    def write_byte(self, byte):
        self.output.write(byte)


    def write_bits(self, value, bits):
        mask = (1 << bits) - 1
        for _ in range(bits):
            self.write_bit(value >> (bits-1))
            value = value << 1 & mask


    def close(self):
        while self.buffersize != 0:
            self.write_bit(0)
        self.output.close()


    def get_totalbytes(self):
        return self.totalbytes



def open_inout(input: str, output: str):
    bit_in = BitInputStream(
        open(input, "rb")
    )
    bit_out = BitOutputStream(
        open(output, "wb")
    )

    return bit_in, bit_out


def open_inin(input1: str, input2: str):
    in1 = BitInputStream(
        open(input1, "rb")
    )
    in2 = BitInputStream(
        open(input2, "rb")
    )

    return in1, in2


def close_stream(*files):
    for f in files:
        f.close()