import argparse
import logging

from .pyeval import AlgebraEval
from .tokenizer import SyntaxError

CMD_CHAR = "#"

algebra_eval = AlgebraEval()


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


def pre_parse(cmd:str, args) -> str:
    match cmd:
        case "tree":
            args.v = True
            return "Tree display enabled"
        case "notree":
            args.v = False 
            return "Tree display disabled"
        case _:
            return "Invalid command!"



def main() -> None:
    logging.basicConfig(
        format="{asctime}: {levelname} - {name} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="./pypratt.log",
        filemode="w",  # Overwrite the log file each time
        level=logging.INFO,
    )

    parser = init_parser()
    args = parser.parse_args()

    if not args.base or args.base < 2:
        print("Base must be a positive integer greater than 1.")
        raise SystemExit

    print("Welcome to the Algebra Evaluator")
    print("You can enter algebraic expressions at the prompt or press enter to exit.")
    # print("The supported operators are: +, -, *, /, ^ and brackets.")
    if args.v:
        print(
            "Parse tree display enabled."
        )

    if args.base != 10:
        print(f"Using base {args.base} for evaluation.")
        algebra_eval.set_base(args.base)

    
    while True:
        expr = input("> ").strip()
        if not expr.strip():
            print("Ciao!")
            break

        if expr[0] == CMD_CHAR:
            msg = pre_parse(expr[1:].strip(), args)
            args.v = not args.v
            print(f"Verbose mode {'enabled' if args.v else 'disabled'}.")
            continue

        try:
            result: str = algebra_eval.evaluate(expr)
            print(result)
            if args.v:
                print()
                print(algebra_eval.get_parse_tree())
                print()
        except ValueError as e:
            print(f"{e}")
        except SyntaxError as e:
            print(f"Syntax error: {e}")


main()
