from dataclasses import dataclass
from os import path

from .. import DATA_PATH


@dataclass(slots=True)
class Plot:
    coords: tuple[int, int]
    plant: str
    neighbors: list["Plot"]
    visited: bool = False

    def __hash__(self) -> int:
        return hash(self.coords)

    def __lt__(self, other):
        if self.coords[0] == other.coords[0]:
            return self.coords[1] < other.coords[1]
        return self.coords[0] < other.coords[1]


def read_input(filename: str) -> dict[tuple[int, int], Plot]:
    plots = {}
    with open(path.join(DATA_PATH, filename), "r") as fh:
        for row, line in enumerate(fh.read().strip().split("\n")):
            for col, plant in enumerate(line):
                plots[(row, col)] = Plot((row, col), plant, [])

    for (row, col), plot in plots.items():
        neighbor_indices = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

        for neighbor_index in neighbor_indices:
            try:
                neighbor = plots[neighbor_index]
            except KeyError:
                continue

            if plot.plant == neighbor.plant:
                plot.neighbors.append(neighbor)

    return plots


def calculate_fence_cost(plot: Plot, perimeter: int = 0, area: int = 0) -> tuple[int, int]:
    perimeter += 4 - len(plot.neighbors)
    area += 1

    plot.visited = True
    for neighbor in plot.neighbors:
        if neighbor.visited:
            continue
        perimeter, area = calculate_fence_cost(neighbor, perimeter, area)

    return perimeter, area


def get_connected_plots(plot: Plot, region: set[tuple[int, int]] = set()) -> set[tuple[int, int]]:
    region = region.union({plot.coords})
    plot.visited = True

    for plot in plot.neighbors:
        region = get_connected_plots(plot, region) if not plot.visited else region

    return region


def get_num_corners(coord: tuple[int, int], coords: set[tuple[int, int]]) -> int:
    row, col = coord

    num_corners = 0
    for d_row in (1, -1):
        for d_col in (1, -1):
            if (row + d_row, col) not in coords and (row, col + d_col) not in coords:
                num_corners += 1
            elif (
                (row + d_row, col) in coords
                and (row, col + d_col) in coords
                and (row + d_row, col + d_col) not in coords
            ):
                num_corners += 1

    return num_corners


def part1(filename: str) -> int:
    plots = read_input(filename)

    cost = 0
    for plot in plots.values():
        if plot.visited:
            continue
        perimeter, area = calculate_fence_cost(plot)
        cost += perimeter * area

    return cost


def part2(filename: str) -> int:
    plots = read_input(filename)

    for plot in plots.values():
        plot.visited = False

    cost = 0
    for plot in plots.values():
        if plot.visited:
            continue

        region = get_connected_plots(plot)
        num_corners = sum(get_num_corners(p, region) for p in region)
        cost += len(region) * num_corners

    return cost


assert part1("day12-sample.txt") == 140
assert part1("day12-sample2.txt") == 772
assert part1("day12-sample3.txt") == 1930
assert part1("day12.txt") == 1464678

assert part2("day12-sample.txt") == 80
assert part2("day12-sample2.txt") == 436
assert part2("day12-sample3.txt") == 1206
assert part2("day12-sample4.txt") == 236
assert part2("day12-sample5.txt") == 368
assert part2("day12.txt") == 877492
