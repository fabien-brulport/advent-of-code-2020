from dataclasses import dataclass
from pathlib import Path
from typing import List


DATA_PATH = Path(__file__).resolve().parents[1] / "data"


@dataclass
class Line:
    first_number: int
    second_number: int
    letter: str
    password: str

    @classmethod
    def from_str(cls, line: str) -> "Line":
        rule, password = line.split(": ")
        numbers, letter = rule.split(" ")
        first_number, second_number = numbers.split("-")
        return cls(
            first_number=int(first_number),
            second_number=int(second_number),
            letter=letter,
            password=password,
        )

    def is_valid_part_1(self) -> bool:
        count = self.password.count(self.letter)
        return self.first_number <= count and count <= self.second_number

    def is_valid_part_2(self) -> bool:
        return (self.password[self.first_number - 1] == self.letter) != (
            self.password[self.second_number - 1] == self.letter
        )


def read_input(path: Path) -> List[Line]:
    data = path.read_text().strip("\n").split("\n")
    return [Line.from_str(line) for line in data]


def main(problem_number: int):
    data = read_input(DATA_PATH / f"input_{problem_number}.txt")
    print(sum(line.is_valid_part_1() for line in data))
    print(sum(line.is_valid_part_2() for line in data))
