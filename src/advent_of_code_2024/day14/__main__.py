from os import path

from .. import DATA_PATH


def part1(filename: str, max_x: int, max_y: int) -> int:
    q1, q2, q3, q4 = 0, 0, 0, 0

    half_max_x = max_x // 2
    half_max_y = max_y // 2

    with open(path.join(DATA_PATH, filename), "r") as fh:
        while line := fh.readline():
            pos, vel = line.strip().split(" ")
            x, y = map(int, pos[2:].split(","))
            dx, dy = map(int, vel[2:].split(","))

            final_x = (x + 100 * dx) % max_x
            final_y = (y + 100 * dy) % max_y

            if final_x == half_max_x or final_y == half_max_y:
                continue

            if final_x < half_max_x:
                if final_y < half_max_y:
                    q1 += 1
                else:
                    q2 += 1
            else:
                if final_y < half_max_y:
                    q3 += 1
                else:
                    q4 += 1

    return q1 * q2 * q3 * q4


def safety_score(x: list[int], y: list[int], half_max_x: int, half_max_y: int) -> int:
    q1, q2, q3, q4 = 0, 0, 0, 0

    for x_, y_ in zip(x, y):
        if x_ == half_max_x or y_ == half_max_y:
            continue

        if x_ < half_max_x:
            if y_ < half_max_y:
                q1 += 1
            else:
                q2 += 1
        else:
            if y_ < half_max_y:
                q3 += 1
            else:
                q4 += 1

    return q1 * q2 * q3 * q4


def part2(filename: str, max_x: int, max_y: int) -> int:
    half_max_x = max_x // 2
    half_max_y = max_y // 2

    min_safety = 1e12
    min_round = -1
    x, y, dx, dy = [], [], [], []
    with open(path.join(DATA_PATH, filename), "r") as fh:
        while line := fh.readline():
            pos, vel = line.strip().split(" ")
            x_, y_ = map(int, pos[2:].split(","))
            dx_, dy_ = map(int, vel[2:].split(","))
            x.append(x_)
            y.append(y_)
            dx.append(dx_)
            dy.append(dy_)

    safeties = []
    for idx in range(7709, 7710):
        final_x = [(x_ + idx * dx_) % max_x for x_, dx_ in zip(x, dx)]
        final_y = [(y_ + idx * dy_) % max_y for y_, dy_ in zip(y, dy)]

        safety = safety_score(final_x, final_y, half_max_x, half_max_y)
        safeties.append(safety)
        if safety < min_safety:
            min_round = idx
            min_safety = safety
    
    return min_round


assert part1("day14-sample.txt", 11, 7) == 12
assert part1("day14.txt", 101, 103) == 230435667

assert part2("day14.txt", 101, 103) == 7709
