"""Compile an AST into C code."""
from abstract_syntax_tree import ASTNode, tokens_to_ast, ASTNodeTypes
from lexer import lex
main_content = open("lib_c/main.c", "r", encoding="utf-8").read()

def compile_ast(tree: ASTNode) -> None:
    """Compile the given tree into a C file."""
    compilation = ""
    compilation += tree.compile()
    compilation += tree.delimiter()
    for child in tree.children:
        compilation += child.compile()
        compilation += child.delimiter()
    return compilation

def compile_file(source_file: str, output_file: str) -> None:
    """Compile the given Python file into a C file."""
    source_code = open(source_file, "r", encoding="utf-8").read()
    main = ASTNode(node_type=ASTNodeTypes.ENTRYPOINT)
    tokens_to_ast(lex(source_code), main)
    main = main_content.replace("// %main", compile_ast(main))

    with open(output_file, "w") as output:
        output.write(main)
