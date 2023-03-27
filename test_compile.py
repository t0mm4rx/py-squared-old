"""Test the abstract syntax tree implementation."""
from compile import compile_file

compile_file("./samples/print.py", "./build/print.c")