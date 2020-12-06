from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple


DATA_PATH = Path(__file__).resolve().parents[1] / "data"


@dataclass
class Group:
    answers: List[str]

    @classmethod
    def from_str(cls, group: str) -> "Group":
        return cls(answers=group.split("\n"))

    def count_part1(self) -> int:
        set_answer = set(char for string in self.answers for char in string)
        return len(set_answer)

    def count_part2(self) -> int:
        if len(self.answers) == 1:
            return self.count_part1()

        set_answer = set(self.answers[0])
        for answer in self.answers[1:]:
            set_answer = set_answer.intersection(answer)
        return len(set_answer)


def read_input(path: Path) -> List[Group]:
    groups = path.read_text().strip("\n").split("\n\n")
    return [Group.from_str(group) for group in groups]


def main(problem_number: int):
    data = read_input(DATA_PATH / f"input_{problem_number}.txt")

    print(sum(group.count_part1() for group in data))
    print(sum(group.count_part2() for group in data))
