from dataclasses import dataclass
from os import path

from .. import DATA_PATH


@dataclass(slots=True)
class TrailLocation:
    coords: tuple[int, int]
    height: int
    connections: list["TrailLocation"]

    def __hash__(self) -> int:
        return hash((self.coords, self.height))


def read_data(filename: str) -> dict[tuple[int, int], TrailLocation]:
    locations: dict[tuple[int, int], TrailLocation] = {}
    with open(path.join(DATA_PATH, filename), "r") as fh:
        heights = [[int(value) for value in line] for line in fh.read().strip().split("\n")]

    num_rows, num_cols = len(heights), len(heights[0])
    for row in range(num_rows):
        for col in range(num_cols):
            locations[(row, col)] = TrailLocation((row, col), heights[row][col], [])

    for row in range(num_rows):
        for col in range(num_cols):
            height = heights[row][col]
            maybe_neighbors = [
                locations[coords]
                for coords in [
                    (row - 1, col) if row > 0 else None,
                    (row + 1, col) if row < num_rows - 1 else None,
                    (row, col - 1) if col > 0 else None,
                    (row, col + 1) if col < num_cols - 1 else None,
                ]
                if coords is not None
            ]
            neighbors = [neighbor for neighbor in maybe_neighbors if height + 1 == neighbor.height]
            print(row, col, height, *map(lambda x: (x.height, x.coords), neighbors))
            locations[(row, col)].connections = neighbors

    return locations


def step(location: TrailLocation) -> list[tuple[TrailLocation, ...]]:
    if location.height == 9:
        return [(location,)]
    else:
        paths = []
        for connection in location.connections:
            for remaining in step(connection):
                here_to_end = tuple((location, *remaining))
                paths.append(here_to_end)

        return paths


def part1(filename: str) -> int:
    locations = read_data(filename)
    roots = {coord: 0 for coord, location in locations.items() if location.height == 0}

    score = 0
    for root_coord in roots.keys():
        root_location = locations[root_coord]
        paths_from_root = step(root_location)
        unique_endpoints = set(p[-1] for p in paths_from_root)
        score += len(unique_endpoints)

    return score


def part2(filename: str) -> int:
    locations = read_data(filename)
    roots = {coord: 0 for coord, location in locations.items() if location.height == 0}

    rating = 0
    all_paths: list[tuple[TrailLocation, ...]] = []
    for root_coord in roots.keys():
        root_location = locations[root_coord]
        paths_from_root = step(root_location)
        rating += len(paths_from_root)
        all_paths.extend(paths_from_root)

    return rating


assert part1("day10-sample.txt") == 36
assert part1("day10.txt") == 538

assert part2("day10-sample.txt") == 81
assert part2("day10.txt") == 1110
