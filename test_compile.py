"""Test the abstract syntax tree implementation."""
from compile import compile_file

compile_file("./samples/int_declaration.py", "./build/int_declaration.c")
