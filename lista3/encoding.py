class Encoding():
    """Abstract class for encoding."""

    def __init__(self, out):
        self.output = out 

    def write(self, num):
        code = self.encode(num)
        for bit in code:
            self.output.write_bit(int(bit))

    def encode(self, num):
        return NotImplementedError()


def _gamma_encode(num):
    binary = bin(num)
    prefix_len = len(binary) - 3
    return prefix_len*'0' + binary[2:]


class Gamma(Encoding):
    """Elias gamma encoding."""

    def encode(self, num):
        return _gamma_encode(num)


class Delta(Encoding):
    """Elias delta encoding."""

    def encode(self, num):
        binary = bin(num)
        bin_len = len(binary) - 2
        prefix = _gamma_encode(bin_len)
        return prefix + binary[3:]


class Omega(Encoding):
    """Elias omega encoding."""

    def encode(self, num):
        if num == 0:
            print(num)
        result = '0'
        k = num
        while k > 1:
            binary_k = bin(k)
            result = binary_k[2:] + result
            k = len(binary_k) - 3
        return result


class Fibonacci(Encoding):
    """Fibonacci encoding."""

    def __init__(self, out):
        Encoding.__init__(self, out)

    def encode(self, num):
        
        def fib(n):
            if n in [0,1]:
                return 1
            return fib(n-1) + fib(n-2)

        i = 1
        while fib(i+1) <= num:
            i += 1
        binary = ''
        while i > 0:
            if fib(i) <= num:
                binary = '1' + binary
                num -= fib(i)
            else:
                binary = '0' + binary
            i -= 1
        return binary + '1'
