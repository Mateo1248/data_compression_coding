

class Decoding():
    """Abstract class for encoding."""

    def __init__(self, inp):
        self.input = inp  

    def read(self):
        return NotImplementedError()


class Gamma(Decoding):
    """Elias gamma decoding."""

    def read(self):
        zero_counter = 0
        bit = self.input.read_bit()
        while bit == 0:
            zero_counter += 1
            bit = self.input.read_bit()
        if bit == -1:
            return -1
        binary = str(bit)
        for _ in range(zero_counter):
            bit = self.input.read_bit()
            if bit == -1:
                raise EOFError()
            binary += str(bit)

        return int(binary, 2)


class Delta(Decoding):
    """Elias delta decoding."""

    def read(self):
        zero_counter = 0
        bit = self.input.read_bit()
        while bit == 0:
            zero_counter += 1
            bit = self.input.read_bit()
        if bit == -1:
            return -1
        len_binary = str(bit)
        for _ in range(zero_counter):
            bit = self.input.read_bit()
            if bit == -1:
                raise EOFError()
            len_binary += str(bit)
        binary = '1'
        for _ in range(int(len_binary, 2)-1):
            bit = self.input.read_bit()
            if bit == -1:
                raise EOFError()
            binary += str(bit)
        return int(binary, 2)


class Omega(Decoding):
    """Elias omega decoding."""

    def __init__(self, inp):
        super().__init__(inp)
        self.flag = False

    def read(self):
        num = 1
        bit = self.input.read_bit()
        if bit == -1:
            return -1
        while bit != 0:
            binary = str(bit)
            for _ in range(num):
                bit = self.input.read_bit()
                if bit == -1:
                    return -1
                binary += str(bit)
            num = int(binary, 2)
            bit = self.input.read_bit()
            if bit == -1:
                return -1
        # if num > 1:
        #     self.flag = True
        return num


class Fibonacci(Decoding):
    """Fibonacci decoding."""

    def __init__(self, inp):
        Decoding.__init__(self, inp)

    def read(self):

        def fib(n):
            if n in [0,1]:
                return 1
            return fib(n-1) + fib(n-2)

        old_bit = self.input.read_bit()
        new_bit = self.input.read_bit()
        if new_bit == -1:
            return -1
        binary = str(old_bit)
        while not old_bit == new_bit == 1:
            old_bit = new_bit
            binary += str(old_bit)
            new_bit = self.input.read_bit()
            if new_bit == -1:
                return -1
        num = 0
        bin_len = len(binary)
        for i in range(bin_len):
            if binary[i] == '1':
                num += fib(i+1)
        return num