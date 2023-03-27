"""Test the abstract syntax tree implementation."""
from abstract_syntax_tree import print_ast, tokens_to_ast, ASTNode, ASTNodeTypes
from lexer import lex

source_code = open("./samples/print.py", "r", encoding="utf-8").read()

main = ASTNode(node_type=ASTNodeTypes.ENTRYPOINT)
tokens_to_ast(lex(source_code), main)
print_ast(main)
