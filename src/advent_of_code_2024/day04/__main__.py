from collections import Counter
from itertools import product
from os import path

from .. import DATA_PATH


def xmas_check(location: tuple[int, int], offsets: tuple[int, int], lines: list[str]) -> bool:
    row_idx, col_idx = location
    row_offset, col_offset = offsets

    for idx, letter in enumerate("XMAS"):
        try:
            row = row_idx + idx * row_offset
            col = col_idx + idx * col_offset
            # need this so we cannot wrap around
            assert row >= 0 and col >= 0
            assert lines[row][col] == letter
        except (IndexError, AssertionError):
            return False

    return True


def mas_check(location: tuple[int, int], offsets: tuple[int, int], lines: list[str]) -> tuple[int, int] | None:
    row_idx, col_idx = location
    row_offset, col_offset = offsets

    for idx, letter in enumerate("MAS"):
        try:
            row = row_idx + idx * row_offset
            col = col_idx + idx * col_offset
            # need this so we cannot wrap around
            assert row >= 0 and col >= 0
            assert lines[row][col] == letter
        except (IndexError, AssertionError):
            return None

    return (row_idx + row_offset, col_idx + col_offset)


def part1(filename: str) -> int:
    with open(path.join(DATA_PATH, filename), "r") as fh:
        lines: list[str] = [line.strip() for line in fh.readlines()]

    num_rows, num_cols = len(lines), len(lines[0])
    offsets: list[tuple[int, int]] = [loc for loc in product(range(-1, 2), repeat=2) if loc != (0, 0)]  # type: ignore

    num_xmas = 0
    for row_idx, col_idx in product(range(num_rows), range(num_cols)):
        if lines[row_idx][col_idx] == "X":
            num_xmas += sum(xmas_check((row_idx, col_idx), offset, lines) for offset in offsets)

    return num_xmas


def part2(filename: str) -> int:
    with open(path.join(DATA_PATH, filename), "r") as fh:
        lines: list[str] = [line.strip() for line in fh.readlines()]

    num_rows, num_cols = len(lines), len(lines[0])
    offsets: list[tuple[int, int]] = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    mas_locations = []
    for row_idx, col_idx in product(range(num_rows), range(num_cols)):
        if lines[row_idx][col_idx] == "M":
            mas_locations.extend([mas_check((row_idx, col_idx), offset, lines) for offset in offsets])

    return sum(v == 2 for k, v in Counter(mas_locations).items() if k is not None)


assert part1("day04-sample.txt") == 18
assert part1("day04.txt") == 2613

assert part2("day04-sample.txt") == 9
assert part2("day04.txt") == 1905
