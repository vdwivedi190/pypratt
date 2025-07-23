import pytest

from .tokenizer import tokenize, SyntaxError
from .parser import parse, _evaluate_tree

invalid_expressions = [
    "  ",
    "+",
    "1 +",
    " + 1",
    " 1.0 + ",
]

unmatched_brackets = [
    "1 + (2 * 3",
    "1 + 2 * 3)",
    "(1 + 2) * (3 + 4))",
    "(1 + 2) * (3 + 4.))",
    "((1 + 2) * (3 + 4)",
]

# List of valid expressions for testing along with their number of tokens
# (including an END token) and expected result
valid_expressions_int = [
    ("1 + 2", 4, 3.0),
    ("1 + 2 + 3", 6, 6.0),
    ("1 + 2 * 3", 6, 7.0),
    ("1 * 2 + 3", 6, 5.0),
    ("1 + 2 * 3 + 4", 8, 11.0),
    ("1 * 2 + 3 * 4", 8, 14.0),
    ("1 * 2 + 3 / 4", 8, 2.75),
    ("1 + 2 * 3 ^ 4", 8, 163.0),
    ("2 ^ 3 / 4 - 1", 8, 1.0),
    ("0 - 1", 4, -1.0),
    ("0 - 1.2", 4, -1.2),
]

valid_expressions_float = [
    ("1.0 + 2.0", 4, 3.0),
    ("1.0 + 2.0 + 3.0", 6, 6.0),
]


valid_expressions_int_with_brackets = [
    ("2 + (3 + 4)", 8, 9.0),
    ("(2 + 3) + 4", 8, 9.0),
    ("2 * (3 + 4)", 8, 14.0),
    ("(2 + 3) * 4", 8, 20.0),
    ("2 (3 + 4)", 8, 14.0),
    ("(2 + (3 + 4))", 10, 9.0),
    ("(1 + 2) * (3 + 4)", 12, 21.0),
    ("(1 + 2) (3 + 4)", 12, 21.0),
    ("((1 + 2) * 3) ^ 2", 12, 81.0),
]


# ============================================
# TOKENIZER TESTS


@pytest.mark.parametrize("expr", invalid_expressions)
def test_tokenizer_invalid_expr(expr):
    with pytest.raises(SyntaxError):
        tokenize(expr)


@pytest.mark.parametrize("expr", unmatched_brackets)
def test_tokenizer_unmatched_brackets(expr):
    with pytest.raises(SyntaxError):
        tokenize(expr)


@pytest.mark.parametrize(
    "expr, num_tokens",
    [(expr, num_tokens) for expr, num_tokens, _ in valid_expressions_int],
)
def test_tokenizer_valid_expr_int(expr, num_tokens):
    tokens = tokenize(expr)
    assert len(tokens) == num_tokens


@pytest.mark.parametrize(
    "expr, num_tokens",
    [(expr, num_tokens) for expr, num_tokens, _ in valid_expressions_float],
)
def test_tokenizer_valid_expr_float(expr, num_tokens):
    tokens = tokenize(expr)
    assert len(tokens) == num_tokens


@pytest.mark.parametrize(
    "expr, num_tokens",
    [(expr, num_tokens) for expr, num_tokens, _ in valid_expressions_int_with_brackets],
)
def test_tokenizer_valid_expr_int_with_brackets(expr, num_tokens):
    tokens = tokenize(expr)
    assert len(tokens) == num_tokens


# ============================================
# PARSER TESTS


# ============================================
# EVAL TESTS


@pytest.mark.parametrize(
    "expr, expected", [(expr, expected) for expr, _, expected in valid_expressions_int]
)
def test_eval_valid_expr_int(expr, expected):
    result = _evaluate_tree(parse(tokenize(expr)))
    assert result == expected


@pytest.mark.parametrize(
    "expr, expected",
    [(expr, expected) for expr, _, expected in valid_expressions_float],
)
def test_eval_valid_expr_float(expr, expected):
    result = _evaluate_tree(parse(tokenize(expr)))
    assert result == expected


@pytest.mark.parametrize(
    "expr, expected",
    [(expr, expected) for expr, _, expected in valid_expressions_int_with_brackets],
)
def test_eval_valid_expr_int_with_brackets(expr, expected):
    result = _evaluate_tree(parse(tokenize(expr)))
    assert result == expected
