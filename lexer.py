"""
This file contains methods to lex the source file, aka removing whitespaces and converting
the source string to an array of tokens.

This is the first step of parsing.
"""
from dataclasses import dataclass
from enum import Enum, auto

class TokenTypes(Enum):
    """Type of tokens."""
    PARENTHESIS_OPEN	= auto()
    PARENTHESIS_CLOSE	= auto()
    COLON				= auto()
    EQUALS				= auto()
    LITERAL				= auto()

@dataclass
class Token:
    """A container for a token in the source code."""
    token_type: TokenTypes
    line_position: int
    row_position: int
    value: str | None = None

KEYWORDS: dict[str, TokenTypes] = {
    "(": TokenTypes.PARENTHESIS_OPEN,
    ")": TokenTypes.PARENTHESIS_CLOSE,
    ":": TokenTypes.COLON,
    "=": TokenTypes.EQUALS,
}

def word_to_token(word: str, line_position: int, row_position: int) -> Token:
    """Convert a word into a Token."""
    if word in KEYWORDS:
        return Token(
            token_type=KEYWORDS[word],
            line_position=line_position,
            row_position=row_position,
        )
    return Token(
        token_type=TokenTypes.LITERAL,
        line_position=line_position,
        row_position=row_position,
        value=word,
    )

def lex(source: str) -> list[Token]:
    """Convert the given source string as an array of tokens."""
    tokens: list[Token] = []
    for line_position, line in enumerate(source.split("\n")):
        current_word = ""
        for row_position, char in enumerate(line):
            if char == " ":
                if len(current_word) > 0:
                    tokens.append(word_to_token(
                        current_word,
                        line_position,
                        row_position,
                    ))
                    current_word = ""
                current_word = ""
                continue
            if char in KEYWORDS:
                if len(current_word) > 0:
                    tokens.append(word_to_token(
                        current_word,
                        line_position,
                        row_position,
                    ))
                    current_word = ""
                tokens.append(
                    word_to_token(
                        char,
                        line_position,
                        row_position,
                    ),
                )
            else:
                current_word += char
        if len(current_word) > 0:
            tokens.append(word_to_token(
                current_word,
                line_position,
                row_position,
            ))
    return tokens
