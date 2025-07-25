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


def num_to_str(num: int | float, base: int) -> str:
    """Convert the result (float) to the given base as a string"""
    if base == 10:
        return str(num)
    else:
        sign, int_digits, frac_digits = num_to_base(num, base)
        sign_str = "-" if sign == -1 else ""
        int_part_str = "".join(num_to_digit_char(digit, base) for digit in int_digits)
        if not frac_digits:
            return sign_str + int_part_str
        else:
            frac_part_str = "".join(
                num_to_digit_char(digit, base) for digit in frac_digits
            )
            return sign_str + int_part_str + DECIMAL_POINT + frac_part_str


def str_to_float(expr: str, base: int) -> float:
    """Convert a string to a number in the specified base."""
    if not str:
        raise ValueError("Empty string cannot be converted to a number.")

    num:float = 0.0
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
    return num


def str_to_int(expr: str, base: int) -> float:
    """Convert a string to a number in the specified base."""
    if not str:
        raise ValueError("Empty string cannot be converted to a number.")

    num:int = 0
    for char in expr:
        if char == DECIMAL_POINT:
            raise ValueError(
                f"Integer expected, but encountered a decimal point."
            )
        elif char == SEPARATOR:
            continue
        else:
            try:
                digit = digit_char_to_num(char, base)
            except ValueError:
                raise
            num = num * base + digit
    return num


def num_to_base(num: int | float, base: int) -> tuple[int, list[int], list[int]]:
    """Convert a number to a string representation in the specified base.

    Returns a tuple of two lists corresponding to the integer and fractional parts.
    This function works for any base > 2
    """

    if base < 2:
        raise ValueError("Base must be a positive integer greater than 1.")

    int_digits = []
    frac_digits = []

    sign = 1 if num >= 0 else -1
    num = abs(num)

    int_part = int(num)
    frac_part = num - int_part

    # Convert integer part
    while int_part > 0:
        int_digits.append(int_part % base)
        int_part //= base
    int_digits.reverse()

    # Convert fractional part
    if frac_part > 0:
        count = 0
        while frac_part > 0 and count < MAX_DIGITS_AFTER_DECIMAL:
            digit = int(frac_part * base)
            frac_part *= base
            digit = int(frac_part)
            frac_part -= digit
            frac_digits.append(digit)
            count += 1

    return (sign, int_digits, frac_digits)
