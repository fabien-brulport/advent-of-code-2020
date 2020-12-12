from dataclasses import dataclass
import math
from pathlib import Path
from typing import List


DATA_PATH = Path(__file__).resolve().parents[1] / "data"


@dataclass
class Instruction:
    symbol: str
    number: int

    @classmethod
    def from_str(cls, line: str) -> "Instruction":
        return Instruction(symbol=line[0], number=int(line[1:]))


@dataclass
class Position:
    direction: str
    x: int
    y: int

    def update(self, instruction: Instruction):
        symbol = instruction.symbol
        if symbol == "F":
            symbol = self.direction

        if symbol == "N":
            self.y += instruction.number
        elif symbol == "S":
            self.y -= instruction.number
        elif symbol == "E":
            self.x += instruction.number
        elif symbol == "W":
            self.x -= instruction.number
        elif symbol == "L" or symbol == "R":
            directions = ["N", "W", "S", "E"]
            # Go in reverse direction if "R"
            sign = 1 if symbol == "L" else -1
            current_idx = directions.index(self.direction)
            next_idx = (current_idx + sign * (instruction.number // 90)) % 4
            self.direction = directions[next_idx]
        else:
            raise ValueError


@dataclass
class Wayback:
    x: int
    y: int

    def update(self, instruction: Instruction):
        if instruction.symbol == "N":
            self.y += instruction.number
        elif instruction.symbol == "S":
            self.y -= instruction.number
        elif instruction.symbol == "E":
            self.x += instruction.number
        elif instruction.symbol == "W":
            self.x -= instruction.number
        elif instruction.symbol == "L" or instruction.symbol == "R":
            angle = math.radians(instruction.number)
            if instruction.symbol == "R":
                angle *= -1
            # Using round to keep integers
            self.x, self.y = (
                round(self.x * math.cos(angle) - self.y * math.sin(angle)),
                round(self.x * math.sin(angle) + self.y * math.cos(angle)),
            )
        else:
            raise ValueError


def read_input(path: Path) -> List[Instruction]:
    return list(map(Instruction.from_str, path.read_text().strip("\n").split("\n")))


def main(problem_number: int):
    list_instruction = read_input(DATA_PATH / f"input_{problem_number}.txt")

    # Part 1
    position = Position(direction="E", x=0, y=0)
    for instruction in list_instruction:
        position.update(instruction)

    print(abs(position.x) + abs(position.y))

    # Part 2
    wayback = Wayback(x=10, y=1)
    position = Position(direction="E", x=0, y=0)

    for instruction in list_instruction:
        if instruction.symbol == "F":
            position.x += wayback.x * instruction.number
            position.y += wayback.y * instruction.number
        else:
            wayback.update(instruction)

    print(abs(position.x) + abs(position.y))
