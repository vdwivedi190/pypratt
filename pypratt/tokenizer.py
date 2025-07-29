from enum import Enum

from .num_utils import DECIMAL_POINT, SEPARATOR
from .operators import (
    BINARY_OP_SYMS,
    POSTFIX_UNARY_OP_SYMS,
    PREFIX_UNARY_OP_SYMS,
    OPEN_BRACKETS,
    CLOSE_BRACKETS,
    MATCHING_BRACKET,
    OP_START_SYM,
)


class SyntaxError(Exception):
    """Custom exception for tokenization errors.

    This exception contains an additional "index" attribute to indicate the
    position of the error in the expression."""

    def __init__(self, message: str, index: int):
        super().__init__(message)
        self.message = message
        self.index = index


class TokenTypes(Enum):
    NUMBER = "NUMBER"
    PREFIX_UNARY_OP = "PREFIX_UNARY_OP"
    POSTFIX_UNARY_OP = "POSTFIX_UNARY_OP"
    BINARY_OP = "BINARY_OP"
    OPEN_BRACKET = "OPEN_BRACKET"
    CLOSE_BRACKET = "CLOSE_BRACKET"
    END = "END"


class Token:
    def __init__(self, type: TokenTypes, value: str, distance: int | None = None):
        self.type: TokenTypes = type
        self.value = value
        self.distance: int | None = distance
        # Used for brackets to indicate distance to matching bracket

    def __repr__(self):
        match self.type:
            case TokenTypes.NUMBER:
                return f"#[{self.value}]"
            case TokenTypes.PREFIX_UNARY_OP | TokenTypes.POSTFIX_UNARY_OP | TokenTypes.BINARY_OP:
                return f"Op[{self.value}]"
            case TokenTypes.OPEN_BRACKET:
                return "[Open Bracket]"
            case TokenTypes.CLOSE_BRACKET:
                return "[Close Bracket]"
            case TokenTypes.END:
                return "[END]"
            case _:
                return "[Invalid Token!]"

    def __str__(self):
        match self.type:
            case TokenTypes.NUMBER:
                return self.value
            case TokenTypes.PREFIX_UNARY_OP | TokenTypes.POSTFIX_UNARY_OP | TokenTypes.BINARY_OP:
                return f"[{self.value}]"
            case TokenTypes.OPEN_BRACKET:
                return "[Open Bracket]"
            case TokenTypes.CLOSE_BRACKET:
                return "[Close Bracket]"
            case TokenTypes.END:
                return "[END]"
            case _:
                return "[INVALID]"


def tokenize(expr: str, *, base: int) -> list[Token]:
    """Tokenize the input expression into a list of tokens."""

    tokens: list[Token] = []
    cur_str = ""
    bracket_stack: list[int] = []

    # Add a space at the end of the expression to process the last number
    # expr = expr.replace(" ", "")
    expr += " "
    for str_index, char in enumerate(expr):
        if is_valid_str_token(char):
            cur_str += char
        else:
            # If the previous character was part of a number, convert it to a NumberToken first
            if cur_str:
                if cur_str[0] == OP_START_SYM:
                    if cur_str[1:] in BINARY_OP_SYMS:
                        add_operator_token(tokens, cur_str[1:], str_index)
                    else:
                        raise SyntaxError(f"Encountered invalid operator {cur_str}", str_index)
                elif is_valid_num(cur_str, base):
                    tokens.append(Token(TokenTypes.NUMBER, cur_str))
                elif is_valid_var(cur_str):
                    tokens.append(Token(TokenTypes.NUMBER, cur_str))
                else:
                    raise SyntaxError(
                        f"'{cur_str}' is not a valid number or variable name.",
                        str_index,
                    )
                cur_str = ""

            if char in POSTFIX_UNARY_OP_SYMS:
                if not tokens:
                    raise SyntaxError(
                        f"Expression cannot start with a postfix operator '{char}'!",
                        str_index,
                    )
                elif tokens[-1].type not in {
                    TokenTypes.NUMBER,
                    TokenTypes.CLOSE_BRACKET,
                }:
                    raise SyntaxError(
                        f"The postfix operator '{char}' must follow a number or a closing bracket!",
                        str_index,
                    )
                tokens.append(Token(TokenTypes.POSTFIX_UNARY_OP, char))

            elif char in BINARY_OP_SYMS:
                add_operator_token(tokens, char, str_index)

            elif char in OPEN_BRACKETS:
                # Assume that an opening bracket preceeded by a number or a closing bracket implies multiplication
                if tokens and (
                    tokens[-1].type == TokenTypes.NUMBER
                    or tokens[-1].type == TokenTypes.CLOSE_BRACKET
                ):
                    tokens.append(Token(TokenTypes.BINARY_OP, "*"))
                tokens.append(Token(TokenTypes.OPEN_BRACKET, char))
                bracket_stack.append(len(tokens) - 1)

            elif char in CLOSE_BRACKETS:
                if not tokens or tokens[-1].type in {
                    TokenTypes.BINARY_OP,
                    TokenTypes.OPEN_BRACKET,
                }:
                    raise SyntaxError(
                        f"Expression cannot end with a closing bracket '{char}'!",
                        str_index,
                    )
                try:
                    opening_index = bracket_stack.pop()
                except IndexError:
                    raise SyntaxError(
                        f"Closing bracket: {char} without matching opening bracket",
                        str_index,
                    )
                if MATCHING_BRACKET[char] != tokens[opening_index].value:
                    raise SyntaxError(
                        f"Mismatched brackets: {tokens[opening_index].value} closed with {char}",
                        str_index,
                    )

                tokens.append(Token(TokenTypes.CLOSE_BRACKET, char))
                compute_bracket_distances(tokens, opening_index)

            elif char != " ":
                raise SyntaxError(f"Unexpected character: {char}", str_index)

    if not tokens:
        raise SyntaxError("Expression cannot be empty!", 0)

    if bracket_stack:
        raise SyntaxError("Encountered unmatched closing brackets:", len(expr) - 1)

    if tokens[-1].type == TokenTypes.BINARY_OP:
        raise SyntaxError(
            f"Expression cannot end with a binary operator '{tokens[-1].value}'",
            len(expr) - 1,
        )

    tokens.append(Token(TokenTypes.END, ""))
    return tokens


def add_operator_token(tokens:list[Token], op:str, str_index:int):
    if not tokens:
        raise SyntaxError(
                        f"Expression cannot start with a binary operator '{op}'!",
                        str_index,
                    )
    elif tokens[-1].type == TokenTypes.BINARY_OP:
        raise SyntaxError(
                        f"The binary operator '{op}' cannot follow another binary operator!",
                        str_index,
                    )
    elif tokens[-1].type == TokenTypes.OPEN_BRACKET:
        raise SyntaxError(
                        f"The binary operator '{op}' cannot follow after an opening bracket!",
                        str_index,
                    )
    tokens.append(Token(TokenTypes.BINARY_OP, op))


def compute_bracket_distances(tokens, opening_index):
    cur_index = len(tokens) - 1
    closing_dist = cur_index - opening_index
    tokens[opening_index].distance = closing_dist
    tokens[cur_index].distance = -closing_dist


def is_valid_num(num_str: str, base: int) -> bool:
    """Check if the character is part of a number.

    To account for numbers in different bases, we consider alphanumeric characters,
    decimal points, and separators.
    """
    return all(
        char.isalnum() or char == DECIMAL_POINT or char == SEPARATOR for char in num_str
    )


# TODO: Implement variables!
def is_valid_var(var_str: str) -> bool:
    """Check if a given string corresponds to a preassigned variable"""
    return False


def is_valid_str_token(char: str) -> bool:
    """Check if the character is part of a number.

    To account for numbers in different bases, we consider alphanumeric characters,
    decimal points, and separators.
    """
    return char.isalnum() or char == DECIMAL_POINT or char == SEPARATOR or char == OP_START_SYM
