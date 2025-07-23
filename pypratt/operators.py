OPEN_BRACKETS = {"("}
CLOSE_BRACKETS = {")"}


class BinaryOperator:
    """Enum for binary operators used in expressions."""

    def __init__(self, symbol: str, name: str, precedence: int, function=None):
        self.symbol = symbol
        self.name = name
        self.precedence = precedence
        self.function = function


def add(a: float, b: float) -> float:
    """Function to add two numbers."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Function to subtract two numbers."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Function to multiply two numbers."""
    return a * b


def divide(a: float, b: float) -> float:
    """Function to divide two numbers."""
    if b == 0:
        raise ValueError("Division by zero.")
    return a / b


def exponent(a: float, b: float) -> float:
    """Function to raise a to the power of b."""
    return a**b


OP_ADD = BinaryOperator("+", "ADD", 1, add)
OP_SUBTRACT = BinaryOperator("-", "SUBTRACT", 1, subtract)
OP_MULTIPLY = BinaryOperator("*", "MULTIPLY", 2, multiply)
OP_DIVIDE = BinaryOperator("/", "DIVIDE", 2, divide)
OP_EXPONENT = BinaryOperator("^", "EXPONENT", 3, exponent)

OPS_DICT = {
    OP_ADD.symbol: OP_ADD,
    OP_SUBTRACT.symbol: OP_SUBTRACT,
    OP_MULTIPLY.symbol: OP_MULTIPLY,
    OP_DIVIDE.symbol: OP_DIVIDE,
    OP_EXPONENT.symbol: OP_EXPONENT,
}

BINARY_OPERATORS = {op.symbol for op in OPS_DICT.values()}
