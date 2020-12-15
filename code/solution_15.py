from pathlib import Path
from typing import List


DATA_PATH = Path(__file__).resolve().parents[1] / "data"


def read_input(path: Path) -> List[int]:
    return list(map(int, path.read_text().strip("\n").split(",")))


def play_game(data: List[int], stop_turn: int) -> int:
    """Return the number spoken after ``stop_turn`` rounds of game"""

    # Initialization
    turns = {number: index for index, number in enumerate(data)}
    number = data[-1]

    for turn in range(len(turns), stop_turn):
        # Keeping track of the last_number is needed to have both indexes
        last_number = number
        last_number_turn = turn - 1

        if last_number in turns:
            number = last_number_turn - turns[last_number]
        else:
            number = 0

        # Update the index of the last number
        turns[last_number] = last_number_turn

    return number


def main(problem_number: int):
    data = read_input(DATA_PATH / f"input_{problem_number}.txt")
    print(play_game(data, 2020))
    print(play_game(data, 30_000_000))
