from os import path

from .. import DATA_PATH

"""
    | ax bx | | a | = | target_x |
    | ay by | | b | = | target_y |

    | a | = 1 / det * |  by -bx | | target_x |
    | b |             | -ay  ax | | target_y |
    
"""


def read_two_values(line: str) -> tuple[int, int]:
    _, rest = line.split(": ")
    first, second = map(lambda x: int(x[2:]), rest.split(", "))
    return first, second


def part1(filename: str) -> int:
    with open(path.join(DATA_PATH, filename), "r") as fh:
        games = fh.read().strip().split("\n\n")

    total = 0
    for game in games:
        lines = game.split("\n")

        ax, ay = read_two_values(lines.pop(0))
        bx, by = read_two_values(lines.pop(0))
        target_x, target_y = read_two_values(lines.pop(0))

        det = ax * by - bx * ay
        a = (by * target_x - bx * target_y) / det
        b = (-ay * target_x + ax * target_y) / det

        if a - int(a) < 1e-8 and b - int(b) < 1e-8:
            total += 3 * a + b

    return int(total)


def part2(filename: str) -> int:
    with open(path.join(DATA_PATH, filename), "r") as fh:
        games = fh.read().strip().split("\n\n")

    total = 0
    for game in games:
        lines = game.split("\n")

        ax, ay = read_two_values(lines.pop(0))
        bx, by = read_two_values(lines.pop(0))
        target_x, target_y = read_two_values(lines.pop(0))
        
        target_y += 10000000000000
        target_x += 10000000000000

        det = ax * by - bx * ay
        a = (by * target_x - bx * target_y) / det
        b = (-ay * target_x + ax * target_y) / det

        if a - int(a) < 1e-8 and b - int(b) < 1e-8:
            total += 3 * a + b

    return int(total)




assert part1("day13-sample.txt") == 480
assert part1("day13.txt") == 36571

assert part2("day13-sample.txt") == 875318608908
assert part2("day13.txt") == 85527711500010
