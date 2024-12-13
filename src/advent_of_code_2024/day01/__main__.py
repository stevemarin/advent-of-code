from os import path
from bisect import insort_left
from collections import Counter

from .. import DATA_PATH


def get_difference_part1(filename: str) -> int:
    left, right = [], []
    with open(path.join(DATA_PATH, filename), "r") as fh:
        for line in fh.readlines():
            values = list(map(int, line.strip().split()))
            assert len(values) == 2
            insort_left(left, values[0])
            insort_left(right, values[1])

    difference = 0
    for ll, rr in zip(left, right):
        difference += abs(ll - rr)

    return difference


def get_difference_part2(filename: str) -> int:
    left, right = [], []
    with open(path.join(DATA_PATH, filename), "r") as fh:
        for line in fh.readlines():
            values = list(map(int, line.strip().split()))
            assert len(values) == 2
            left.append(values[0])
            right.append(values[1])

    left = Counter(left)
    right = Counter(right)

    difference = 0
    for val, count in left.items():
        try:
            difference += val * count * right[val]
        except KeyError:
            pass

    return difference


assert get_difference_part1("day01-sample.txt") == 11
assert get_difference_part1("day01.txt") == 2000468

assert get_difference_part2("day01-sample.txt") == 31
assert get_difference_part2("day01.txt") == 18567089