import math


class BitInputStream():
    """Class handling streaming bits from the input."""

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

    def close(self):
        self.input.close()
        self.bitbuffer = -1
        self.buffersize = 0


class BitOutputStream():
    """Class handling streaming bits to the output."""

    def __init__(self, out):
        self.output = out
        self.bitbuffer = 0
        self.buffersize = 0
        self.totalbytes = 0
        self.sym_counter = [0 for _ in range(256)]

    def write_bit(self, bit):
        self.bitbuffer = (self.bitbuffer << 1) | bit
        self.buffersize += 1
        if self.buffersize == 8:
            self.output.write(bytes((self.bitbuffer,)))
            self.totalbytes += 1
            self.sym_counter[self.bitbuffer] += 1
            self.bitbuffer = 0
            self.buffersize = 0

    def close(self):
        while self.buffersize != 0:
            self.write_bit(0)
        self.output.close()

    def get_totalbytes(self):
        return self.totalbytes

    def get_output_entropy(self):
        return sum([x*(math.log(self.totalbytes, 2)-math.log(x, 2)) for x in self.sym_counter if x > 0])/self.totalbytes
