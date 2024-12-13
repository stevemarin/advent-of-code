from itertools import combinations
from math import gcd
from os import path

from .. import DATA_PATH


def read_input(filename: str) -> tuple[dict[str, list[tuple[int, int]]], tuple[int, int]]:
    antennae: dict[str, list[tuple[int, int]]] = {}
    with open(path.join(DATA_PATH, filename), "r") as fh:
        row, col = 0, 0
        for row, line in enumerate(fh.readlines()):
            for col, char in enumerate(line.strip()):
                if char == ".":
                    continue
                if char not in antennae:
                    antennae[char] = [(row, col)]
                else:
                    antennae[char].append((row, col))
    return antennae, (row, col)


def get_antinodes(pt1: tuple[int, int], pt2: tuple[int, int]) -> set[tuple[int, int]]:
    pt1_row, pt1_col = pt1
    pt2_row, pt2_col = pt2
    d_row = pt2_row - pt1_row
    d_col = pt2_col - pt1_col

    return {(pt1_row - d_row, pt1_col - d_col), (pt2_row + d_row, pt2_col + d_col)}


def get_resonant_antinodes(
    pt1: tuple[int, int],
    pt2: tuple[int, int],
    extent: tuple[int, int],
) -> set[tuple[int, int]]:
    pt1_row, pt1_col = pt1
    pt2_row, pt2_col = pt2
    d_row = pt2_row - pt1_row
    d_col = pt2_col - pt1_col

    # in case the antennas are multiple "steps" apart,
    # take gcd to find size of a single step
    the_gcd = gcd(d_row, d_col)
    d_row /= the_gcd
    d_col /= the_gcd

    max_row, max_col = extent

    row, col = pt1

    # add "forward"
    locations = set()
    while 0 <= row <= max_row and 0 <= col <= max_col:
        locations.add((row, col))
        row += d_row
        col += d_col

    # add "backward"
    row, col = pt1
    while 0 <= row <= max_row and 0 <= col <= max_col:
        locations.add((row, col))
        row -= d_row
        col -= d_col

    return locations


def part1(filename: str) -> int:
    antennae, (max_row, max_col) = read_input(filename)

    all_antinodes = set()
    for _, antenna in antennae.items():
        for pt1, pt2 in combinations(antenna, 2):
            all_antinodes |= get_antinodes(pt1, pt2)

    return len(list(filter(lambda x: 0 <= x[0] <= max_row and 0 <= x[1] <= max_col, all_antinodes)))


def part2(filename: str) -> int:
    antennae, extent = read_input(filename)

    all_antinodes = set()
    for _, antenna in antennae.items():
        for pt1, pt2 in combinations(antenna, 2):
            all_antinodes |= get_resonant_antinodes(pt1, pt2, extent)

    return len(all_antinodes)


assert get_antinodes((3, 4), (5, 5)) == {(1, 3), (7, 6)}

assert part1("day08-sample.txt") == 14
assert part1("day08.txt") == 369

assert part2("day08-sample.txt") == 34
assert part2("day08.txt") == 1169
