from collections import defaultdict
from math import log10
from os import path

from .. import DATA_PATH


def blink_once(stone: int) -> tuple[int, ...]:
    if stone == 0:
        return (1,)
    elif (num_digits := int(log10(stone)) + 1) % 2 == 0:
        return divmod(stone, 10 ** (num_digits // 2))
    else:
        return (stone * 2024,)


def blink_multiple(stones: dict[int, int], num_blinks: int) -> dict[int, int]:
    if num_blinks == 0:
        return stones
    else:
        next_stones = defaultdict(int)
        for stone, count in stones.items():
            for res in blink_once(stone):
                next_stones[res] += count

        return blink_multiple(next_stones, num_blinks - 1)


def part1(filename: str, num_blinks) -> int:
    stones = defaultdict(int)
    with open(path.join(DATA_PATH, filename), "r") as fh:
        for stone in map(int, fh.read().strip().split()):
            stones[stone] += 1

    all_stones = defaultdict(int)
    for k, v in blink_multiple(stones, num_blinks).items():
        all_stones[k] += v

    return sum(all_stones.values())


assert part1("day11-sample.txt", 0) == 5
assert part1("day11-sample.txt", 1) == 7
assert part1("day11-sample2.txt", 0) == 2
assert part1("day11-sample2.txt", 1) == 3
assert part1("day11-sample2.txt", 2) == 4
assert part1("day11-sample2.txt", 3) == 5
assert part1("day11-sample2.txt", 4) == 9
assert part1("day11-sample2.txt", 5) == 13
assert part1("day11-sample2.txt", 25) == 55312

assert part1("day11.txt", 25) == 204022
assert part1("day11.txt", 75) == 241651071960597
