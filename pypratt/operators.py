from collections.abc import Callable

type unary_function = Callable[[int | float], int | float]
type binary_function = Callable[[int | float, int | float], int | float]
type function = binary_function | unary_function
# type function = Callable[[int], int] | Callable[[float], float] | Callable[[int,int],int] | Callable[[float, float], float]

OPEN_BRACKETS = ["(", "["]
CLOSE_BRACKETS = [")", "]"]

MATCHING_BRACKET = {
    close_bracket: OPEN_BRACKETS[i] for i, close_bracket in enumerate(CLOSE_BRACKETS)
}


class Operator:
    """Enum for binary operators used in expressions."""

    def __init__(
        self,
        symbol: str,
        name: str,
        precedence: int,
        func: function,
    ):
        self.symbol = symbol
        self.name = name
        self.precedence = precedence
        self.function = func


# DEFINE PREFIX UNARY OPERATORS
OP_NEGATE = Operator(symbol="-", name="NEGATE", precedence=3, func=lambda a: -a)

PREFIX_UNARY_OPS = {
    OP_NEGATE.symbol: OP_NEGATE,
}

PREFIX_UNARY_OP_SYMS = {op.symbol for op in PREFIX_UNARY_OPS.values()}


# DEFINE POSTIX UNARY OPERATORS

FACTORIAL_SYM = "!"
POSTFIX_UNARY_OP_SYMS = {FACTORIAL_SYM}


def factorial(num: int | float) -> int:
    """Calculate factorial of a number."""
    if not isinstance(num, int):
        raise TypeError("Factorial is only defined for integers.")
    elif num < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    elif num == 0 or num == 1:
        return 1
    return num * factorial(num - 1)


OP_FACTORIAL = Operator(
    symbol=FACTORIAL_SYM, name="FACTORIAL", precedence=4, func=factorial
)


POSTFIX_UNARY_OPS = {
    OP_FACTORIAL.symbol: OP_FACTORIAL,
}


# DEFINE (INFIX) BINARY OPERATORS
ADD_SYM = "+"
SUBTRACT_SYM = "-"
MULTIPLY_SYM = "*"
DIVIDE_SYM = "/"
EXPONENT_SYM = "^"
MODULO_SYM = "%"

OP_ADD = Operator(symbol=ADD_SYM, name="ADD", precedence=1, func=lambda a, b: a + b)

OP_SUBTRACT = Operator(
    symbol=SUBTRACT_SYM, name="SUBTRACT", precedence=1, func=lambda a, b: a - b
)

OP_MULTIPLY = Operator(
    symbol=MULTIPLY_SYM, name="MULTIPLY", precedence=2, func=lambda a, b: a * b
)

OP_DIVIDE = Operator(
    symbol=DIVIDE_SYM, name="DIVIDE", precedence=2, func=lambda a, b: a / b
)

OP_EXPONENT = Operator(
    symbol=EXPONENT_SYM, name="EXPONENT", precedence=3, func=lambda a, b: a**b
)

OP_MODULO = Operator(
    symbol=MODULO_SYM, name="MODULO", precedence=2, func=lambda a, b: a % b
)

BINARY_OPS = {
    OP_ADD.symbol: OP_ADD,
    OP_SUBTRACT.symbol: OP_SUBTRACT,
    OP_MULTIPLY.symbol: OP_MULTIPLY,
    OP_DIVIDE.symbol: OP_DIVIDE,
    OP_EXPONENT.symbol: OP_EXPONENT,
    OP_MODULO.symbol: OP_MODULO,
}

BINARY_OP_SYMS = {op.symbol for op in BINARY_OPS.values()}
