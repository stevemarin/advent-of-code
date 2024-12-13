
from functools import cache
from math import log10
from os import path

from .. import DATA_PATH

def blink(stone: int) -> tuple[int, ...]:
    if stone == 0:
        return (1,)
    elif (num_digits := int(log10(stone)) + 1) % 2 == 0:
        return divmod(stone, 10 ** (num_digits // 2))
    else:
        return (stone * 2024,)
    
@cache
def blink_multiple(stones: tuple[int, ...], num_blinks: int) -> tuple[int, ...]:
    print("on blink...", num_blinks)
    if num_blinks == 0:
        return stones
    else:
        next_stones: list[int] = []
        for stone in stones:
            next_stones.extend(blink(stone))
        
        return blink_multiple(tuple(next_stones), num_blinks - 1)


def part1(filename: str, num_blinks) -> int:
    with open(path.join(DATA_PATH, filename), "r") as fh:
        stones = map(int, fh.read().strip().split())
    
    all_stones = []
    for stone in stones:
        all_stones.extend(blink_multiple((stone,), num_blinks))

    return len(all_stones)


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

print(part1("day11.txt", 75))