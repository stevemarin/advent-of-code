from collections.abc import Callable
from itertools import product
from os import path

from .. import DATA_PATH


def add(a: int, b: int) -> int:
    return a + b


def mul(a: int, b: int) -> int:
    return a * b


def concat(a: int, b: int) -> int:
    return int(str(a) + str(b))


Operator = Callable[[int, int], int]

# idea: start from end using operators -, /, substr to speed up

def valid(result: int, operands: list[int], operators: tuple[Operator, ...]) -> bool:
    assert len(operators) == len(operands) - 1
    current = operands[0]
    for value, op in zip(operands[1:], operators):
        current = op(current, value)
        if current > result:
            return False

    return current == result


def part1(filename: str) -> int:
    valid_sum = 0
    with open(path.join(DATA_PATH, filename), "r") as fh:
        for line in fh.readlines():
            value, tmp = line.strip().split(": ")
            result = int(value)
            operands = list(map(int, tmp.split()))
            for operators in product((add, mul), repeat=len(operands) - 1):
                if valid(result, operands, operators):
                    valid_sum += result
                    break

    return valid_sum


def part2(filename: str) -> int:
    valid_sum = 0
    with open(path.join(DATA_PATH, filename), "r") as fh:
        for line in fh.readlines():
            value, tmp = line.strip().split(": ")
            result = int(value)
            operands = list(map(int, tmp.split()))
            for operators in product((add, mul, concat), repeat=len(operands) - 1):
                if valid(result, operands, operators):
                    valid_sum += result
                    break

    return valid_sum


assert part1("day07-sample.txt") == 3749
assert part1("day07.txt") == 975671981569

assert part2("day07-sample.txt") == 11387
assert part2("day07.txt") == 223472064194845
