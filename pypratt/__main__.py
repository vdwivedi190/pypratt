import argparse

from .pyeval import AlgebraEval
from .tokenizer import SyntaxError


def init_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pypratt",
        description="A pratt parser for simple algebraic expressions.",
        usage="python -m %(prog)s [OPTIONS] message",
    )

    parser.add_argument(
        "-b",
        "--base",
        metavar="BASE",
        type=int,
        default=10,
        help="Base for the evaluation (default = 10)",
    )

    parser.add_argument(
        "-v",
        action="store_true",
        help="Verbose mode: Display the parse tree",
    )

    return parser


def main() -> None:
    parser = init_parser()
    args = parser.parse_args()

    if not args.base or args.base < 2:
        print("Base must be a positive integer greater than 1.")
        raise SystemExit

    print("Welcome to the Algebra Evaluator")
    print("You can enter algebraic expressions at the prompt or press enter to exit.")
    print("The supported operators are: +, -, *, /, ^ and brackets.")
    if args.v:
        print(
            "Verbose mode enabled. The parse tree will be displayed after evaluation."
        )
        print("To toggle this mode, enter #.")
    if args.base != 10:
        print(f"Using base {args.base} for evaluation.")

    algebra_eval = AlgebraEval(base=args.base)
    while True:
        expr = input("> ")
        if not expr.strip():
            print("Ciao!")
            break

        if expr.strip() == "#":
            args.v = not args.v
            print(f"Verbose mode {'enabled' if args.v else 'disabled'}.")
            continue

        try:
            result: str = algebra_eval.evaluate(expr)
            print(result)
            if args.v:
                print()
                algebra_eval.display()
                print()
        # except ValueError as e:
        #     print(f"Value error in expression: {e}")
        except SyntaxError as e:
            print(f"Syntax error in expression: {e}")


main()
