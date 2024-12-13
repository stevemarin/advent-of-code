from dataclasses import dataclass
from os import path

from .. import DATA_PATH


def part1(filename: str) -> int:
    drive = []
    with open(path.join(DATA_PATH, filename), "r") as fh:
        for idx, char in enumerate(fh.read().strip()):
            fileid, remainder = divmod(idx, 2)
            drive.extend([None if remainder != 0 else fileid] * int(char))

    idx = 0
    while True:
        try:
            while drive[idx] is not None:
                idx += 1
            drive[idx] = drive.pop()
        except IndexError:
            break

    return sum(int(v) * idx for idx, v in enumerate(drive))


@dataclass(slots=True)
class File:
    start: int
    length: int
    fileid: int

    def checksum(self) -> int:
        return self.fileid * self.length * (2 * self.start + self.length - 1) // 2


@dataclass(slots=True)
class Gap:
    start: int
    length: int


def part2(filename) -> int:
    files, gaps, start = [], [], 0
    with open(path.join(DATA_PATH, filename), "r") as fh:
        for idx, char in enumerate(fh.read().strip()):
            length = int(char)
            fileid, isfile = idx // 2, idx % 2 == 0

            if isfile:
                files.append(File(start, length, fileid))
            else:
                gaps.append(Gap(start, length))

            start += length

    for file in reversed(files):
        for gap in gaps:
            if gap.start < file.start and gap.length >= file.length:
                file.start = gap.start
                gap.start += file.length
                gap.length -= file.length
                break

    return sum(map(File.checksum, files))


assert part1("day09-sample2.txt") == 60
assert part1("day09-sample.txt") == 1928
assert part1("day09.txt") == 6448989155953

assert part2("day09-sample.txt") == 2858
assert part2("day09.txt") == 6476642796832
