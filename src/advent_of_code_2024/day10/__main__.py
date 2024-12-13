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
    
    def __lt__(self, other) -> bool:
        if self.coords[0] == other.coords[0]:
            return self.coords[1] < other.coords[1]
        return self.coords[0] < other.coords[0]
    
    def __eq__(self, other) -> bool:
        return self.coords == other.coords and self.height == other.height

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


def step(location: TrailLocation, path: tuple[TrailLocation, ...], all_paths: list[tuple[TrailLocation, ...]]) -> None:
    if location.height == 9:
        all_paths.append(path)
    else:
        for connection in location.connections:
            step(connection, tuple((*path, connection)), all_paths)


def part1(filename: str) -> int:
    locations = read_data(filename)
    roots = {coord: 0 for coord, location in locations.items() if location.height == 0}

    all_paths: list[tuple[TrailLocation, ...]] = []
    for root_coord in roots.keys():
        root_location = locations[root_coord]
        step(root_location, (root_location,), all_paths)

    for p in all_paths:
        print(*map(lambda x: x.coords, p))

    counts = {}
    for p in all_paths:
        start, stop = p[0], p[-1]
        if start.coords not in counts:
            counts[start.coords] = set((stop.coords))
        else:
            counts[start.coords].add(stop.coords)
    
    print(counts.keys())
    for k, v in counts.items():
        print(k, len(v))
    
    print(counts)

    # for p in all_paths:
    #     for location in p:
    #         print(location.height, location.coords)
    #     print()
    # str_paths = [
    #     " -> ".join(",".join(str(c) for c in location.coords) for location in one_path) for one_path in all_paths
    # ]
    # print("\n".join(str_paths))

    # print(sorted(all_paths))

    return len(set(all_paths))


print(part1("day10-sample.txt"))
# assert part1("day10-sample.txt") == 36
# print(part1("day10.txt"))

"< 832"
