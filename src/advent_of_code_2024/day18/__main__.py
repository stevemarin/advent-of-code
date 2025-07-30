
def part1(filename: str, size: int) -> int:
    from os import path

    cwd = path.dirname(__file__)
    filename = path.join(cwd, filename)

    grid = [["." for _ in range(size)] for __ in range(size)]
    start, stop = (0, 0), (size - 1, size - 1)

    # initialize dict for shortest path to each point in grid
    # - add boundary with inf steps
    # when each bit corrupts, shortest path is min neighbors + 1
    # - if a pt changes, its neighbors must change too

    with open(filename, "r") as fh:
        for _ in range(12):
            row, col = map(int, fh.readline().strip().split(","))
            grid[col][row] = "#"

    for row in grid:
        print("".join(row))

    return -1

if __name__ == "__main__":
    part1("sample.data", 7)