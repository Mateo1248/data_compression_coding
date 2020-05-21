"""LZW algorithm."""
import math
import collections as cl

EOF_CODE = 257


class LZWEncoder():
    """Class encoding files with LZW algorithm."""

    def __init__(self, dictionary, input_file, output_encoder, dict_set):
        self.dict_set = dict_set
        self.dict:dict = dictionary
        self.input = input_file
        self.output_encoder = output_encoder
        self.totalbytes = 0
        self.sym_counter = cl.Counter()

    def encode(self):
        prefix = b''
        byte = self.input.read(1)
        while byte:
            self.totalbytes += 1
            self.sym_counter[byte[0]] += 1
            prefbyt = prefix + byte
            if prefbyt in self.dict_set:
                prefix += byte
            else:
                self.output_encoder.write(self.dict[prefix]+1)
                self.dict[prefbyt] = len(self.dict)
                self.dict_set.add(prefbyt)
                prefix = byte
            byte = self.input.read(1)
        self.output_encoder.write(self.dict[prefix]+1)
        self.output_encoder.write(EOF_CODE)  # EOF

    def get_totalbytes(self):
        return self.totalbytes

    def get_input_entropy(self):
        return sum([x*(math.log(self.totalbytes,2)-math.log(x,2)) for x in self.sym_counter if x > 0])/self.totalbytes


class LZWDecoder():
    """Class decoding files with LZW algorithm."""

    def __init__(self, dictionary, output_file, input_decoder):
        self.dict = dictionary
        self.output = output_file
        self.input_decoder = input_decoder

    def decode(self):
        old_input = self.input_decoder.read()-1
        if old_input < 0:
            return
        s = self.dict[old_input]
        self.output.write(s)
        new_input = self.input_decoder.read()
        c = bytes((s[0],))
        while new_input > 0:
            new_input -= 1
            if new_input < 0 or new_input >= len(self.dict):
                s = self.dict[old_input]
                s += c
            else:
                s = self.dict[new_input]
            self.output.write(s)
            c = bytes((s[0],))
            self.dict.append(self.dict[old_input]+c)
            old_input = new_input
            new_input = self.input_decoder.read()
            if new_input == EOF_CODE:
                break
