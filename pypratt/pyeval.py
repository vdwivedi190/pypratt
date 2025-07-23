from .tokenizer import tokenize
from .parser import Node, parse, display_tree
from .parser import evaluate_tree


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
        self.tokens = tokenize(self.expr, base=self.base)
        self.tree_root = parse(self.tokens)
        self.result = evaluate_tree(self.tree_root, self.base)

        # print(f"Evaluating expression '{self.expr}' in base {self.base}")
        # print("Tokens:")
        # print_tokens(self.tokens)
        # print("Parsed Tree:")
        # display_tree(self.tree_root)

        return self.result

    def display(self) -> None:
        """Display the expression and its evaluation."""
        if self.tree_root:
            print("PARSE TREE:")
            display_tree(self.tree_root)
