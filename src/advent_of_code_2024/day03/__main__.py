from os import path

from .. import DATA_PATH


def get_char(idx: int, chars: str) -> tuple[int, str]:
    return idx + 1, chars[idx]


def peek(n: int, idx: int, chars: str) -> str:
    return chars[idx : idx + n]


def match(m: str, idx: int, chars: str) -> tuple[int, bool]:
    if peek(len(m), idx, chars) == m:
        return idx + len(m), True
    else:
        return idx, False


def read_multiply(idx: int, chars: str) -> tuple[int, int]:
    initial_idx = idx

    idx, matched = match("ul(", idx, chars)
    if not matched:
        return initial_idx, 0

    idx, digits = get_char(idx, chars)
    if not "0" <= digits <= "9":
        return initial_idx, 0

    for _ in range(2):
        idx, char = get_char(idx, chars)
        if not "0" <= char <= "9":
            idx -= 1
            break
        else:
            digits += char

    lhs = int(digits)

    idx, comma = get_char(idx, chars)
    if comma != ",":
        return initial_idx, 0

    idx, digits = get_char(idx, chars)
    if not "0" <= digits <= "9":
        return initial_idx, 0

    for _ in range(2):
        idx, char = get_char(idx, chars)
        if not "0" <= char <= "9":
            idx -= 1
            break
        else:
            digits += char

    rhs = int(digits)

    idx, matched = match(")", idx, chars)
    if not matched:
        return initial_idx, 0

    return idx, lhs * rhs

def read_switch(enabled: bool, idx: int, chars: str) -> tuple[int, bool]:
    initial_idx = idx

    idx, matched = match("o()", idx, chars)
    if matched:
        return idx, True
    
    idx, matched = match("on't()", idx, chars)
    if matched:
        return idx, False
    
    return initial_idx, enabled

 
def part1(filename: str) -> int:
    with open(path.join(DATA_PATH, filename), "r") as fh:
        chars = fh.read()

    total, idx = 0, 0
    while True:
        try:
            idx, char = get_char(idx, chars)
        except IndexError:
            break

        match char:
            case "m":
                idx, value = read_multiply(idx, chars)
                total += value
            case _:
                pass

    return total


def part2(filename: str) -> int:
    with open(path.join(DATA_PATH, filename), "r") as fh:
        chars = fh.read()

    enabled, total, idx = True, 0, 0
    while True:
        try:
            idx, char = get_char(idx, chars)
        except IndexError:
            break

        match char:
            case "m":
                idx, value = read_multiply(idx, chars)
                if enabled:
                    total += value
            case "d":
                idx, enabled = read_switch(enabled, idx, chars)
            case _:
                pass

    return total


assert part1("day03-sample.txt") == 161
assert part1("day03.txt") == 174103751

assert part2("day03-sample2.txt") == 48
assert part2("day03.txt") == 100411201
