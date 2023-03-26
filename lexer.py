"""
This file contains methods to lex the source file, aka removing whitespaces and converting
the source string to an array of tokens.

This is the first step of parsing.
"""
from dataclasses import dataclass
from enum import Enum, auto

class TokenTypes(Enum):
	PARENTHESIS_OPEN	= auto()
	PARENTHESIS_CLOSE	= auto()
	LITERAL			= auto()

@dataclass
class Token:
	token_type: TokenTypes
	line_position: int
	row_position: int

def word_to_token(word: str, line: int, row: int) -> Token:
	"""Convert a word into a Token."""
	new_token = Token()
	new_token.line_position = line
	new_token.row_position = row
	if word == "(":
		new_token.token_type = TokenTypes.PARENTHESIS_OPEN
	elif word == ")":
		new_token.token_type = TokenTypes.PARENTHESIS_CLOSE
	else:
		new_token.token_type = TokenTypes.LITERAL

def lex(source: str) -> list[Token]:
	"""Convert the given source string as an array of tokens."""
	tokens: list[Token] = []
	for line_number, line in enumerate(source.split("\n")):
		current_word = ""
		for row_number, char in enumerate(line):
			if char == " ":
				current_word = ""
				continue
			if char == "(" or char == ")":
				if len(current_word) > 0:
					tokens.append(word_to_token(current_word, line_number, row_number))
					current_word = ""
				tokens.append(word_to_token(char))
			else:
				current_word += char
	return tokens

