from dataclasses import dataclass
from pathlib import Path
import re
from typing import List, Tuple


DATA_PATH = Path(__file__).resolve().parents[1] / "data"


@dataclass
class Instruction:
    command: str
    number: int

    @classmethod
    def from_str(cls, line: str) -> "Instruction":
        match = re.match(r"^(?P<command>\w{3}) (?P<number>[+-]\d*)$", line)
        return cls(command=match.group("command"), number=int(match.group("number")))


def read_input(path: Path) -> List[Instruction]:
    data = path.read_text().strip("\n").split("\n")
    instructions = [Instruction.from_str(line) for line in data]
    return instructions


def run_program(program: List[Instruction]) -> Tuple[bool, int]:
    """
    Run the program and return 2 values:

      - a bool, True if the program has terminated normally (no infinite loop)
      - an int, the accumulator
    """
    index_visited = []
    current_idx = 0
    accumulator = 0
    while True:
        if current_idx in index_visited:
            return False, accumulator

        if current_idx >= len(program):
            return True, accumulator

        index_visited.append(current_idx)
        instruction = program[current_idx]
        if instruction.command == "nop":
            current_idx += 1
        elif instruction.command == "jmp":
            current_idx += instruction.number
        elif instruction.command == "acc":
            current_idx += 1
            accumulator += instruction.number
        else:
            raise ValueError(f"{instruction}")


def main(problem_number: int):
    data = read_input(DATA_PATH / f"input_{problem_number}.txt")
    # Part 1
    is_infinite, accumulator = run_program(data)
    print(accumulator)

    # Part 2
    for instruction in data:
        # Change the command if it's a nop or jmp, then run the program
        # and change back the command
        if instruction.command == "nop":
            instruction.command = "jmp"
            terminated, accumulator = run_program(data)
            instruction.command = "nop"

        elif instruction.command == "jmp":
            instruction.command = "nop"
            terminated, accumulator = run_program(data)
            instruction.command = "jmp"
        else:
            continue

        if terminated:
            print(accumulator)
            break
