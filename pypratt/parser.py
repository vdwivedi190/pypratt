from .operators import BINARY_OPS
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
            display_tree(node.left, indent + "     ")
            return
        else:
            print(indent + "├──", end="")
            display_tree(node.left, indent + "│    ")
            print(indent + "└──", end="")
            display_tree(node.right, indent + "     ")
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
        elif token.type == TokenTypes.POSTFIX_UNARY_OP:
            op_node = Node(token)
            op_node.left = root
            root = op_node
        elif token.type == TokenTypes.BINARY_OP:
            op_node = Node(token)
            cur_prec = BINARY_OPS[token.value].precedence
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
