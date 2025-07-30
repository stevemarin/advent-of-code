from dataclasses import dataclass


@dataclass(slots=True)
class Machine:
    a: int
    b: int
    c: int
    instructions: list[int]

    ip: int = 0
    buffer: None | list[int] = None

    def op(self, opcode: int, operand: int):
        combo = [0, 1, 2, 3, self.a, self.b, self.c]
        match opcode:
            case 0:
                self.a >>= combo[operand]
            case 1:
                self.b ^= operand
            case 2:
                self.b = combo[operand] % 8
            case 3:
                if self.a != 0:
                    self.ip = operand - 2
            case 4:
                self.b ^= self.c
            case 5:
                if self.buffer is None:
                    self.buffer = [combo[operand] % 8]
                else:
                    self.buffer.append(combo[operand] % 8)
            case 6:
                self.b = self.a >> combo[operand]
            case 7:
                self.c = self.a >> combo[operand]

    def run(self):
        while True:
            try:
                opcode, operand = self.instructions[self.ip : self.ip + 2]
            except ValueError:
                break

            self.op(opcode, operand)
            self.ip += 2


def part1(filename: str) -> str:
    from os import path

    cwd = path.dirname(__file__)
    filename = path.join(cwd, filename)

    with open(filename, "r") as fh:
        registers, instructions = fh.read().strip().split("\n\n")

    a, b, c = (int(line.split(":")[1]) for line in registers.split("\n"))
    instructions = list(map(int, instructions.split(":")[1].strip().split(",")))

    machine = Machine(a, b, c, instructions)
    machine.run()

    if machine.buffer is None:
        return ""
    else:
        return ",".join(map(str, machine.buffer))


def part2(filename: str) -> int:
    from os import path

    cwd = path.dirname(__file__)
    filename = path.join(cwd, filename)

    with open(filename, "r") as fh:
        _, instructions = fh.read().strip().split("\n\n")

    instructions = list(map(int, instructions.split(":")[1].strip().split(",")))

    a = 0
    while True:
        machine = Machine(a, 0, 0, instructions)
        machine.run()

        matches = 0
        assert machine.buffer is not None
        for val1, val2 in zip(reversed(instructions), reversed(machine.buffer)):
            if val1 == val2:
                matches += 1
            else:
                break

        if matches == len(instructions):
            return a

        a += int(8 ** (len(instructions) - matches - 1))


if __name__ == "__main__":
    machine = Machine(-1, -1, 9, [2, 6])
    machine.run()
    assert machine.b == 1

    machine = Machine(10, -1, -1, [5, 0, 5, 1, 5, 4])
    machine.run()
    assert machine.buffer == [0, 1, 2]

    machine = Machine(2024, -1, -1, [0, 1, 5, 4, 3, 0])
    machine.run()
    assert machine.buffer == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
    assert machine.a == 0

    machine = Machine(-1, 29, -1, [1, 7])
    machine.run()
    assert machine.b == 26

    machine = Machine(-1, 2024, 43690, [4, 0])
    machine.run()
    assert machine.b == 44354

    assert part1("sample.data") == "4,6,3,5,6,3,5,2,1,0"
    assert part1("in.data") == "6,1,6,4,2,4,7,3,5"

    assert part2("sample2.data") == 117440
    assert part2("in.data") == 202975183645226
