from os import path

from .. import DATA_PATH


def update_direction(delta_row: int, delta_col: int) -> tuple[int, int]:
    match (delta_row, delta_col):
        case (-1, 0):
            return 0, 1
        case (0, 1):
            return 1, 0
        case (1, 0):
            return 0, -1
        case (0, -1):
            return -1, 0
        case _:
            raise ValueError()


def read_input(filename: str) -> tuple[int, int, list[list[str]]]:
    row, col, area = 0, 0, []
    with open(path.join(DATA_PATH, filename), "r") as fh:
        for row_idx, line in enumerate(fh.readlines()):
            if "^" in line:
                row, col = row_idx, line.index("^")
                line = line.replace("^", ".")
            area.append(list(line.strip()))

    return row, col, area


def walk_area(row: int, col: int, area: list[list[str]]) -> set[tuple[int, int]]:
    seen_locations = {(row, col)}
    delta_row, delta_col = -1, 0

    while True:
        try:
            if row + delta_row < 0 or col + delta_col < 0:
                return seen_locations
            next_symbol = area[row + delta_row][col + delta_col]
        except IndexError:
            return seen_locations

        if next_symbol != "#":
            row += delta_row
            col += delta_col
            seen_locations.add((row, col))
        else:
            delta_row, delta_col = update_direction(delta_row, delta_col)


def loops(row: int, col: int, area: list[list[str]], block: tuple[int, int]) -> bool:
    assert len(block) == 2 and all(map(lambda x: isinstance(x, int), block))

    a = [a[:] for a in area]
    a[block[0]][block[1]] = "#"

    delta_row, delta_col, locations = -1, 0, set()
    while True:
        try:
            if row + delta_row < 0 or col + delta_col < 0:
                return False
            next_symbol = a[row + delta_row][col + delta_col]
        except IndexError:
            return False

        if next_symbol != "#":
            row += delta_row
            col += delta_col
        else:
            # only track locations when hitting a block while moving up
            if delta_row == -1 and delta_col == 0:
                if (row, col) in locations:
                    return True
                else:
                    locations.add((row, col))

            if delta_row == -1 and delta_col == 0:
                locations.add((row, col))

            delta_row, delta_col = update_direction(delta_row, delta_col)


def part1(filename: str) -> int:
    row, col, area = read_input(filename)
    seen_locaions = walk_area(row, col, area)
    return len(seen_locaions)


def part2(filename: str) -> int:
    row, col, area = read_input(filename)
    seen_locations = walk_area(row, col, area)
    return sum(loops(row, col, area, block) for block in seen_locations)


assert part1("day06-sample.txt") == 41
assert part1("day06.txt") == 4826

assert part2("day06-sample.txt") == 6
assert part2("day06.txt") == 1721
