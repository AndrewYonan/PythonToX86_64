#!/bin/bash
python3 src/main.py "$1" run > out.s &&
clang -arch x86_64 out.s -o out &&
./out