"""
Test the lexer.
"""
from lexer import lex

source_code = open("./samples/print.py", "r").read()
print(lex(source_code))

