DECIMAL_POINT = "."
SEPARATOR = ","

MAX_DIGITS_AFTER_DECIMAL = 10


def digit_char_to_num(char: str, base: int = 10) -> int:
    """Convert a single digit character to a number in the specified base."""
    if 2 <= base <= 10:
        if char.isdigit():
            return int(char)
        else:
            raise ValueError(f"Invalid digit '{char}' for base {base}.")
    elif 10 < base < 36:
        if char.isdigit():
            return int(char)
        elif "A" <= char.upper() < chr(ord("A") + base - 10):
            return ord(char.upper()) - ord("A") + 10
        else:
            raise ValueError(f"Invalid digit '{char}' for base {base}.")
    else:
        raise ValueError(f"Base {base} is not supported. Supported bases are 2-36.")


def num_to_digit_char(num: int, base: int) -> str:
    """Convert a number to a string representation in the specified base."""
    if base < 2:
        raise ValueError("Base must be a positive integer greater than 1.")
    if base > 36:
        raise ValueError("Base must be a positive integer less than or equal to 36.")

    if num < 0 or num >= base:
        raise ValueError(f"Digits must be integers between 0 and {base - 1}.")
    elif 0 <= num <= 9:
        return str(num)
    else:
        return chr(ord("A") + num - 10)


def str_to_num(expr: str, base: int = 10) -> float:
    """Convert a string to a number in the specified base."""
    if not str:
        raise ValueError("Empty string cannot be converted to a number.")

    num = 0
    decimal_flag = False
    mul_factor: float = 1

    for char in expr:
        if char == DECIMAL_POINT:
            if decimal_flag:
                raise ValueError(
                    f"Invalid number '{expr}' for base {base}. Multiple decimal points found."
                )
            decimal_flag = True
        elif char == SEPARATOR:
            if decimal_flag:
                raise ValueError(
                    f"Invalid number '{expr}' for base {base}. Separator found after decimal point."
                )
            continue
        else:
            try:
                digit = digit_char_to_num(char, base)
            except ValueError:
                raise
            if decimal_flag:
                mul_factor /= base
                num += digit * mul_factor
            else:
                num = num * base + digit
    return float(num)


def num_to_base(num: float, base: int) -> tuple[list[int], list[int]]:
    """Convert a number to a string representation in the specified base.

    Returns a tuple of two lists corresponding to the integer and fractional parts.
    This function works for any base > 2
    """

    if base < 2:
        raise ValueError("Base must be a positive integer greater than 1.")

    int_part = int(num)
    frac_part = num - int_part

    # Convert integer part
    int_digits = []
    while int_part > 0:
        int_digits.append(int_part % base)
        int_part //= base
    int_digits.reverse()

    # Convert fractional part
    frac_digits = []
    if frac_part > 0:
        count = 0
        while frac_part > 0 and count < MAX_DIGITS_AFTER_DECIMAL:
            digit = int(frac_part * base)
            frac_part *= base
            frac_part, digit = divmod(frac_part, 1)
            frac_digits.append(digit)
            count += 1

    return (int_digits, frac_digits)
