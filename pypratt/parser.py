from .num_utils import DECIMAL_POINT, str_to_num, num_to_base, num_to_digit_char
from .operators import OPS_DICT
from .tokenizer import Token, TokenTypes, SyntaxError


class Node:
    def __init__(self, token: Token | None = None):
        self.token: Token | None = token
        self.left: Node | None = None
        self.right: Node | None = None

    def __repr__(self):
        return f"Node({self.token})"


def display_tree(node: Node | None, indent: str = "  ") -> None:
    """Display the binary tree."""
    if node is not None:
        print(" " + str(node.token))
        if node.left is None:
            return
        elif node.right is None:
            print(indent + "└──", end="")
            display_tree(node.left, indent + "    ")
            return
        else:
            print(indent + "├──", end="")
            display_tree(node.left, indent + "│   ")
            print(indent + "└──", end="")
            display_tree(node.right, indent + "    ")
            return


def parse(tokens: list[Token]) -> Node:
    """Parse the list of tokens into a binary expression tree."""
    if not tokens:
        raise SyntaxError("No tokens to parse", 0)

    root, _ = _parse(tokens)
    return root


def _parse(tokens: list[Token], start: int = 0, prec: int = 0) -> tuple[Node, int]:
    """Internal method to parse tokens into a binary expression tree."""

    token = tokens[start]
    prev_prec = 0

    if token.type == TokenTypes.END:
        raise ValueError("Encountered END token: Something wrong here! ")
    elif token.type == TokenTypes.OPEN_BRACKET:
        root, ind = _parse(tokens, start + 1, prec)
    elif token.type == TokenTypes.NUMBER:
        root = Node(token)
        ind = start + 1
    else:
        raise SyntaxError(
            f"Unexpected token at the beginning of a subtree, got {token.type}", 0
        )

    while ind < len(tokens):
        token = tokens[ind]
        if token.type == TokenTypes.END:
            break
        elif token.type == TokenTypes.NUMBER:
            root.right = Node(token)
        elif token.type == TokenTypes.OPEN_BRACKET:
            node, ind = _parse(tokens, ind + 1, prec)
            root.right = node
        elif token.type == TokenTypes.CLOSE_BRACKET:
            return root, ind + 1
        elif token.type == TokenTypes.OPERATOR:
            op_node = Node(token)
            cur_prec = OPS_DICT[token.value].precedence
            if prev_prec == 0:
                op_node.left = root
                root = op_node
            elif cur_prec > prev_prec:
                node, ind = _parse(tokens, ind - 1, cur_prec)
                root.right = node
            else:
                op_node.left = root
                root = op_node
            prev_prec = cur_prec
        else:
            raise SyntaxError(f"Unexpected token in expression, got {token.type}", ind)
        ind += 1

    return root, ind


def evaluate_tree(root: Node | None, base: int) -> str:
    """Evaluate the binary expression tree."""
    result = _evaluate_tree(root, base)
    print("Raw result:", result)
    # Convert the result (float) to the given base as a string
    if base == 10:
        return str(result)
    else:
        print("Converting result to base", base)
        int_digits, frac_digits = num_to_base(result, base)
        int_part = "".join(num_to_digit_char(digit, base) for digit in int_digits)
        if frac_digits:
            frac_part = "".join(num_to_digit_char(digit, base) for digit in frac_digits)
        else:
            frac_part = "0"  # Ensure at least one digit after decimal
    return f"{int_part}{DECIMAL_POINT}{frac_part}"


def _evaluate_tree(root: Node | None, base: int) -> float:
    if root is None:
        raise ValueError("Cannot evaluate an empty tree.")
    if root.token is None:
        raise ValueError("Cannot evaluate a node without a token.")
    elif root.token.type == TokenTypes.NUMBER:
        return str_to_num(root.token.value, base)
    elif root.token.type == TokenTypes.OPERATOR:
        val_left = _evaluate_tree(root.left, base)
        val_right = _evaluate_tree(root.right, base)
        func = OPS_DICT[root.token.value].function
        if func is None:
            raise ValueError(f"No function defined for operator {root.token.value}.")
        else:
            return func(val_left, val_right)
