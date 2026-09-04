import os
import sys

from parser import *
from compile import *


if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Usage: python3 main.py <command> <python-like file>")
        sys.exit(1)
    
    with open(sys.argv[2], 'r', encoding='utf-8') as py_file:
        prog = py_file.read()
    
    flag = sys.argv[1]

    if (flag == "run"):
        print(compile_x86_64(prog))
    elif (flag == "lex"):
        print(lex(prog))
    