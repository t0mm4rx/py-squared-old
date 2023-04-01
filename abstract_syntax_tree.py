"""AST representation of the source code."""
from dataclasses import dataclass, field
from typing import Any
from enum import Enum, auto
from lexer import Token, TokenTypes
import variables

class ParenthesisNotClose(Exception):
    """Exception raised when a parenthesis is not closed."""

class ASTNodeTypes(Enum):
    """All AST node types."""
    ENTRYPOINT      = auto()
    EXPRESSION      = auto()
    ASSIGNATION     = auto()
    VARIABLE_READ   = auto()
    INT             = auto()
    FUNCTION_CALL   = auto()

@dataclass
class ASTNode:
    """A abstract node."""
    node_type: ASTNodeTypes
    value: Any | None = field(default_factory=lambda: None)
    parent_type: ASTNodeTypes | None = field(default_factory=lambda: None)
    children: list = field(default_factory=lambda: [])

    def compile(self) -> str:
        """Return C code."""
        if self.node_type == ASTNodeTypes.ENTRYPOINT:
            return "// Entrypoint"
        if self.node_type == ASTNodeTypes.INT:
            return f"{self.value}"
        if self.node_type == ASTNodeTypes.FUNCTION_CALL:
            return f"{self.value}({', '.join([ child.compile() for child in self.children ])})"
        if self.node_type == ASTNodeTypes.ASSIGNATION:
            var = variables.variables[self.value]
            return (f"create_variable({var.variable_id}, 8);"
                    f"*((int*)VARIABLES[{var.variable_id}].data) = {self.children[0].compile()}"
                    )
        if self.node_type == ASTNodeTypes.VARIABLE_READ:
            var = variables.variables[self.value]
            return f"""*((int*)VARIABLES[{var.variable_id}].data)"""
        assert False, "Not implemented"

    def delimiter(self) -> str:
        """Do we add a ';' to the end of the node."""
        if self.parent_type in (ASTNodeTypes.ENTRYPOINT,None,):
            return ";\n"
        return ""

def tokens_to_ast(tokens: list[Token], parent_node: ASTNode) -> ASTNode:
    """Parse a token array to an absract syntax tree."""
    cursor = 0
    token_types = [token.token_type for token in tokens[cursor:]]
    while cursor < len(tokens):
        ##
        ##  INT
        ##
        if tokens[cursor].token_type == TokenTypes.LITERAL and tokens[cursor].value.isnumeric():
            parent_node.children.append(
                ASTNode(
                    node_type=ASTNodeTypes.INT,
                    value=int(tokens[cursor].value),
                    parent_type=parent_node.node_type,
                )
            )
            cursor += 1
            continue
        ##
        ##  Variable read
        ##
        if tokens[cursor].token_type == TokenTypes.LITERAL \
           and tokens[cursor].value in variables.variables:
            parent_node.children.append(
                ASTNode(
                    node_type=ASTNodeTypes.VARIABLE_READ,
                    value=tokens[cursor].value,
                    parent_type=parent_node.node_type,
                )
            )
            cursor += 1
            continue
        match token_types[cursor:]:
            ##
            ##  FUNCTION_CALL
            ##
            case [
                TokenTypes.LITERAL,
                TokenTypes.PARENTHESIS_OPEN,
                *following_instructions,
            ]:
                args: list[Token] = []
                args_cursor = cursor + 1 # skip open parenthesis
                while token_types[args_cursor] != TokenTypes.PARENTHESIS_CLOSE:
                    args.append(tokens[args_cursor])
                    args_cursor += 1
                    if args_cursor >= len(token_types):
                        raise ParenthesisNotClose()
                function_node = ASTNode(
                        node_type=ASTNodeTypes.FUNCTION_CALL,
                        value=tokens[cursor].value,
                        parent_type=parent_node.node_type,
                )
                tokens_to_ast(args, function_node)
                parent_node.children.append(function_node)
                cursor = args_cursor
            case [
                TokenTypes.LITERAL,
                TokenTypes.COLON,
                TokenTypes.LITERAL,
                TokenTypes.EQUALS,
                TokenTypes.LITERAL,
                *following_instructions,
            ]:
                assignation_node = ASTNode(
                    node_type=ASTNodeTypes.ASSIGNATION,
                    value=tokens[cursor].value,
                    parent_type=parent_node.node_type,
                )
                tokens_to_ast([tokens[cursor + 4]], assignation_node)
                parent_node.children.append(assignation_node)
                var = variables.Variable(
                    variable_id=variables.current_variable_id,
                    is_primitive=True,
                    primitive_type=variables.PrimitiveTypes.INT,
                )
                variables.current_variable_id += 1
                variables.variables[tokens[cursor].value] = var
                cursor += 4
        cursor += 1

def print_ast(ast: ASTNode, level: int = 1):
    """Print an AST."""
    print(ast.node_type)
    for child in ast.children:
        print(f"{'    ' * level}-> ", end="")
        print_ast(child, level=level + 1)
