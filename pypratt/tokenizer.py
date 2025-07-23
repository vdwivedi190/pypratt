from enum import Enum

from .num_utils import DECIMAL_POINT, SEPARATOR
from .operators import BINARY_OPERATORS, OPEN_BRACKETS, CLOSE_BRACKETS


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
    OPERATOR = "OPERATOR"
    OPEN_BRACKET = "OPEN_BRACKET"
    CLOSE_BRACKET = "CLOSE_BRACKET"
    END = "END"


class Token:
    def __init__(self, type: TokenTypes, value: str, distance: int | None = None):
        self.type: TokenTypes = type
        self.value = value
        self.distance: int | None = distance
        # Used for brackets to indicate distance to matching bracket

    def __str__(self):
        match self.type:
            case TokenTypes.NUMBER:
                return f"#[{self.value}]"
            case TokenTypes.OPERATOR:
                return f"Op[{self.value}]"
            case TokenTypes.OPEN_BRACKET:
                return "[Open Bracket]"
            case TokenTypes.CLOSE_BRACKET:
                return "[Close Bracket]"
            case TokenTypes.END:
                return "[END]"


def tokenize(expr: str, *, base: int = 10) -> list[Token]:
    """Tokenize the input expression into a list of tokens."""

    tokens: list[Token] = []
    num_str = ""
    bracket_stack: list[int] = []

    # Add a space at the end of the expression to process the last number
    expr = expr.replace(" ", "")
    expr += " "
    for str_index, char in enumerate(expr):
        if is_part_of_number(char):
            num_str += char
        else:
            # If the previous character was part of a number, convert it to a NumberToken first
            if num_str:
                tokens.append(Token(TokenTypes.NUMBER, num_str))
                num_str = ""

            if char in BINARY_OPERATORS:
                if not tokens:
                    raise SyntaxError(
                        f"Expression cannot start with a binary operator '{char}'!",
                        str_index,
                    )
                elif tokens[-1].type == TokenTypes.OPERATOR:
                    raise SyntaxError(
                        f"The binary operator '{char}' cannot follow another binary operator!",
                        str_index,
                    )
                elif tokens[-1].type == TokenTypes.OPEN_BRACKET:
                    raise SyntaxError(
                        f"The binary operator '{char}' cannot follow after an opening bracket!",
                        str_index,
                    )
                tokens.append(Token(TokenTypes.OPERATOR, char))

            elif char in OPEN_BRACKETS:
                # Assume that an opening bracket preceeded by a number or a closing bracket implies multiplication
                if tokens and (
                    tokens[-1].type == TokenTypes.NUMBER
                    or tokens[-1].type == TokenTypes.CLOSE_BRACKET
                ):
                    tokens.append(Token(TokenTypes.OPERATOR, "*"))
                tokens.append(Token(TokenTypes.OPEN_BRACKET, char))
                bracket_stack.append(len(tokens) - 1)

            elif char in CLOSE_BRACKETS:
                try:
                    opening_index = bracket_stack.pop()
                except IndexError:
                    raise SyntaxError(
                        f"found closing bracket: {char} without matching opening bracket",
                        str_index,
                    )

                tokens.append(Token(TokenTypes.CLOSE_BRACKET, char))
                cur_index = len(tokens) - 1
                closing_dist = cur_index - opening_index
                tokens[opening_index].distance = closing_dist
                tokens[cur_index].distance = -closing_dist
            elif char != " ":
                raise SyntaxError(f"Unexpected character: {char}", str_index)

    if not tokens:
        raise SyntaxError("Expression cannot be empty!", 0)

    if bracket_stack:
        raise SyntaxError("Encountered unmatched closing brackets:", len(expr) - 1)

    if tokens[-1].type == TokenTypes.OPERATOR:
        raise SyntaxError(
            f"Expression cannot end with a binary operator '{tokens[-1].value}'!",
            len(expr) - 1,
        )

    tokens.append(Token(TokenTypes.END, ""))
    return tokens


def is_part_of_number(char: str) -> bool:
    """Check if the character is part of a number.

    To account for numbers in different bases, we consider alphanumeric characters, decimal points, and separators.
    """
    return char.isalnum() or char == DECIMAL_POINT or char == SEPARATOR


def print_tokens(tokens: list[Token]):
    for index, token in enumerate(tokens):
        print(f" {index}. {token}")
