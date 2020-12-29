from itertools import count
from pathlib import Path
from typing import Tuple

DATA_PATH = Path(__file__).resolve().parents[1] / "data"

SUBJECT_NUMBER = 7
DIVIDER = 20201227


def read_input(path: Path) -> Tuple[int, int]:
    return tuple(int(line) for line in path.read_text().strip("\n").split("\n"))


def find_loop_size(public_key: int) -> int:
    """Find loop size base on the public key"""
    value = 1
    for loop_size in count(1):
        value = (value * SUBJECT_NUMBER) % DIVIDER
        if value == public_key:
            return loop_size


def encrypt(subject_number: int, loop_size: int) -> int:
    """Encrypt a subject number based on the loop size"""
    value = 1
    for _ in range(loop_size):
        value = (value * subject_number) % DIVIDER
    return value


def main(problem_number: int):
    card_public_key, door_public_key = read_input(
        DATA_PATH / f"input_{problem_number}.txt"
    )

    # Part 1
    door_loop_size = find_loop_size(door_public_key)

    encryption_key = encrypt(card_public_key, door_loop_size)
    print(encryption_key)
