import logging

from .tokenizer import tokenize, TokenTypes
from .parser import Node, parse, display_tree
from .operators import PREFIX_UNARY_OPS, POSTFIX_UNARY_OPS, BINARY_OPS
from .num_utils import DECIMAL_POINT, str_to_int, str_to_float, num_to_str


logger = logging.getLogger(__name__)


class AlgebraEval:
    def __init__(self, expr: str = "", *, base: int = 10):
        """Initialize the AlgebraEval with an expression and base."""
        if base < 2:
            raise ValueError("Base must be a positive integer greater than 1.")

        self.expr = expr
        self.base = base
        self.tree_root: Node | None = None

    def evaluate(self, expr: str = "") -> str:
        """Evaluate the algebraic expression."""

        if expr:
            self.expr = expr
        logger.info(f"Evaluating expression '{self.expr}' in base {self.base}")

        self.tokens = tokenize(self.expr, base=self.base)
        logger.info(
            f"Done tokenizing: Found {len(self.tokens)} tokens (including END Token)."
        )
        logger.debug(self.get_tokens())

        self.tree_root = parse(self.tokens)
        logger.info(f"Done parsing.")
        logger.debug(self.get_parse_tree())

        self.result_base10: int | float = _evaluate_parse_tree(
            self.tree_root, self.base
        )
        self.result: str = num_to_str(self.result_base10, self.base)
        logger.info(
            f"{self.expr} =  {self.result_base10} in base 10 = {self.result_base10} in {self.base}"
        )
        return self.result

    def display(self) -> None:
        """Display the expression and its evaluation."""
        if self.tree_root:
            print("PARSE TREE:")
            display_tree(self.tree_root)

    def get_tokens(self) -> str:
        tokens_str = ""
        for index, token in enumerate(self.tokens):
            tokens_str += f" {index}. {token}\n"
        return tokens_str

    def get_parse_tree(self) -> str:
        """Return a string representation of the parse tree"""
        if self.tree_root:
            return _parse_tree_to_str(self.tree_root)
        return "No parse tree available."


def _evaluate_parse_tree(root: Node | None, base: int, int_flag:bool = True) -> int | float:
    """Recursively evaluate the parse tree."""
    if root is None:
        raise ValueError("Cannot evaluate an empty tree.")
    if root.token is None:
        raise ValueError("Cannot evaluate a node without a token.")
    elif root.token.type == TokenTypes.NUMBER:
        if int_flag:
            return str_to_int(root.token.value, base)
        else:
            return str_to_float(root.token.value, base)
    elif root.token.type == TokenTypes.POSTFIX_UNARY_OP:
        val = _evaluate_parse_tree(root.left, base)
        func = POSTFIX_UNARY_OPS[root.token.value].function
        return func(val)
    elif root.token.type == TokenTypes.BINARY_OP:
        val_left = _evaluate_parse_tree(root.left, base)
        val_right = _evaluate_parse_tree(root.right, base)
        func = BINARY_OPS[root.token.value].function
        return func(val_left, val_right)


def _parse_tree_to_str(node: Node | None, indent: str = "  ", prefix: str = "") -> str:
    """Recursively construct a string representation of the parse tree."""
    if node is None:
        return ""
    result = f"{prefix} {str(node.token)}\n"
    if node.left is None and node.right is None:
        return result
    if node.left is not None and node.right is not None:
        result += _parse_tree_to_str(node.left, indent + "│    ", indent + "├──")
        result += _parse_tree_to_str(node.right, indent + "     ", indent + "└──")
    elif node.left is not None:
        result += _parse_tree_to_str(node.left, indent + "     ", indent + "└──")
    return result
