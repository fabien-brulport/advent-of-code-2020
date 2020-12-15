from collections import defaultdict
from pathlib import Path
from typing import List


DATA_PATH = Path(__file__).resolve().parents[1] / "data"


def read_input(path: Path) -> List[int]:
    return list(map(int, path.read_text().strip("\n").split(",")))


def play_game(data: List[int], stop_turn: int) -> int:
    """Return the stop_turn'th number spoken"""
    spoken_numbers = defaultdict(list)
    for turn, number in enumerate(data):
        new_number = number
        spoken_numbers[number].append(turn)

    for turn in range(turn + 1, stop_turn):
        index_list = spoken_numbers[new_number]
        if len(index_list) == 1:
            new_number = 0
        else:
            new_number = index_list[-1] - index_list[-2]

        spoken_numbers[new_number].append(turn)

    return new_number


def main(problem_number: int):
    data = read_input(DATA_PATH / f"input_{problem_number}.txt")
    print(play_game(data, 2020))
    print(play_game(data, 30_000_000))
