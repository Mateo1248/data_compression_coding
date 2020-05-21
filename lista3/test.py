import hashlib as hl
import argparse

argparser = argparse.ArgumentParser(description="Porównaj zawartość plików funkcją hashującą.")
argparser.add_argument("file1")
argparser.add_argument("file2")
args = argparser.parse_args()

with open(args.file1, "rb") as bin3:
    with open(args.file2, "rb") as xd:
        str1 = hl.md5(bin3.read()).hexdigest()
        str2 = hl.md5(xd.read()).hexdigest()

        print(args.file1, str1)
        print(args.file2, str2)
        print("Równe:", str1==str2)