from dataclasses import dataclass


def flatten(s: list[list[str]]) -> list[str]:
    return [item for sublist in s for item in sublist]


@dataclass(slots=True)
class Coord:
    row: int
    col: int

    def __add__(self, other) -> "Coord":
        return Coord(self.row + other.row, self.col + other.col)

    def __mul__(self, n: int) -> "Coord":
        assert isinstance(n, int)
        return Coord(self.row * n, self.col * n)

    def __hash__(self) -> int:
        return hash((self.row, self.col))


@dataclass(slots=True)
class Map:
    _rows: list[list[str]]

    def __getitem__(self, coord: Coord) -> str:
        return self._rows[coord.row][coord.col]

    def __repr__(self):
        return "\n".join("".join(row) for row in self._rows)

    def __setitem__(self, src: Coord, dst: Coord) -> None:
        self._rows[dst.row][dst.col], self._rows[src.row][src.col] = self._rows[src.row][src.col], "."

    def robot(self) -> Coord:
        for row_idx, row in enumerate(self._rows):
            if "@" in row:
                return Coord(row_idx, row.index("@"))
        else:
            raise ValueError("cannot find robot!!!")

    def gps(self) -> int:
        value = 0
        for row_idx, row in enumerate(self._rows):
            for col_idx, char in enumerate(row):
                if char == "O" or char == "[":
                    value += row_idx * 100 + col_idx
        return value

    def widen(self) -> "Map":
        replacements = {"#": ["#", "#"], "O": ["[", "]"], ".": [".", "."], "@": ["@", "."]}
        return Map([flatten([replacements[char] for char in row]) for row in self._rows])


class CannotMoveError(Exception):
    pass


def get_valid_moves(themap: Map, start: Coord, offset: Coord, queue: list[Coord]) -> list[Coord]:
    queue = [start]
    dest = start + offset

    match themap[dest], offset.row:
        case ".", _:
            return queue + [start]
        case "O", _:
            return queue + get_valid_moves(themap, dest, offset, queue)
        case d, 0 if d in "[]":
            return queue + get_valid_moves(themap, dest, offset, queue)
        case d, o if d in "[]" and o != 0:
            step = 1 if d == "[" else -1
            other = get_valid_moves(themap, dest + Coord(0, step), offset, queue)
            return other + queue + get_valid_moves(themap, dest, offset, queue)
        case "#", _:
            raise CannotMoveError
        case d:
            raise ValueError("unexpected dest:", d)


def part1(filename: str, widen: bool = False) -> int:
    from os import path

    cwd = path.dirname(__file__)
    filename = path.join(cwd, filename)

    with open(filename, "r") as fh:
        grid, directions = fh.read().strip().split("\n\n")

    themap = Map(list(map(lambda x: list(x), grid.split("\n"))))
    if widen:
        themap = themap.widen()

    robot = themap.robot()

    for direction in directions:
        if direction == "\n":
            continue

        offset = {"v": Coord(1, 0), "^": Coord(-1, 0), "<": Coord(0, -1), ">": Coord(0, 1)}[direction]
        try:
            valid_moves = get_valid_moves(themap, robot, offset, [])
            robot += offset
        except CannotMoveError:
            continue

        seen = set()
        for start in reversed(valid_moves):
            if start not in seen:
                seen.add(start)
                themap[start] = start + offset

    return themap.gps()


def part2(filename: str) -> int:
    return part1(filename, widen=True)


if __name__ == "__main__":
    assert part1("sample.data") == 2028
    assert part1("sample2.data") == 10092
    assert part1("in.data") == 1511865

    assert part2("sample2.data") == 9021
    assert part2("in.data") == 1519991
