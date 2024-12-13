from os import path
from itertools import pairwise

from advent_of_code_2024 import DATA_PATH


def check_no_dampening(values: list[int]) -> bool:
    sign = 1 if values[0] - values[1] < 0 else -1
    for v1, v2 in pairwise(values):
        if not 0 < sign * (v2 - v1) < 4:
            return False
    return True


def check_dampening(values: list[int]) -> bool:
    sign = 1 if values[0] - values[1] < 0 else -1

    for idx, (v1, v2) in enumerate(pairwise(values)):
        if not 0 < sign * (v2 - v1) < 4:
            break
    else:
        return True

    for bad_idx in range(idx - 1, idx + 2):
        if check_no_dampening(values[:bad_idx] + values[bad_idx + 1:]):
            return True

    return False


def part1(filename: str) -> int:
    with open(path.join(DATA_PATH, filename), "r") as fh:
        safe = 0
        for line in fh.readlines():
            values = list(map(int, line.split()))
            if check_no_dampening(values):
                safe += 1

    return safe


def part2(filename: str) -> int:
    with open(path.join(DATA_PATH, filename), "r") as fh:
        safe = 0
        for line in fh.readlines():
            values = list(map(int, line.split()))
            if check_dampening(values):
                safe += 1

    return safe


assert part1("day02-sample.txt") == 2
assert part1("day02.txt") == 624

assert part2("day02-sample.txt") == 4
assert part2("day02.txt") == 658
