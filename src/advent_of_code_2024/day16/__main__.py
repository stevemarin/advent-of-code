from collections import defaultdict
from heapq import heappush, heappop

# my answers were a little wordy, so I tried implementing this:
# https://www.reddit.com/r/adventofcode/comments/1hfboft/comment/m2bcfmq/


def parts(filename: str) -> tuple[int, int]:
    from os import path

    cwd = path.dirname(__file__)
    filename = path.join(cwd, filename)

    with open(filename, "r") as fh:
        grid = {
            row_num + col_num * 1j: char
            for row_num, row in enumerate(fh.read().strip().split("\n"))
            for col_num, char in enumerate(row)
        }

    (start,) = (k for k, v in grid.items() if v == "S")
    (stop,) = (k for k, v in grid.items() if v == "E")

    min_cost = int(1e9)
    min_cost_at_coord = defaultdict(lambda: int(1e9))
    coords_on_min_paths = set()

    # these values are:
    # - cost
    # - tiebreaker (so we don't need to sort the complex numbers)
    # - current coordinate
    # - current direction (columns are imaginary, so +j is moving right/east in map)
    # - current path thus far
    heap = [(0, tiebreaker := 0, start, 1j, [start])]

    while heap:
        cost, _, coord, heading, path = heappop(heap)

        # key: any min path must have a min cost at each location
        if cost > min_cost_at_coord[coord, heading]:
            continue
        else:
            min_cost_at_coord[coord, heading] = cost

        if coord == stop and cost <= min_cost:
            coords_on_min_paths |= set(path)
            min_cost = cost

        # multiplying by +/-1j is a +/- 90 degree rotation
        for rotation, step_cost in (1, 1), (1j, 1001), (-1j, 1001):
            next_heading = heading * rotation
            next_coord = coord + next_heading
            if grid[next_coord] == "#":
                continue

            heappush(
                heap, (cost + step_cost, tiebreaker := tiebreaker + 1, next_coord, next_heading, path + [next_coord])
            )

    return min_cost, len(coords_on_min_paths)


if __name__ == "__main__":
    assert parts("sample.data") == (7036, 45)
    assert parts("sample2.data") == (11048, 64)
    assert parts("in.data") == (102460, 527)
