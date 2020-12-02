from itertools import combinations
from pathlib import Path
from typing import List


DATA_PATH = Path(__file__).resolve().parents[1] / "data"


def read_input(path: Path) -> List[int]:
    return list(map(int, path.read_text().strip("\n").split("\n")))
    

def main(problem_number: int):
    data = read_input(DATA_PATH / f"input_{problem_number}.txt")
    for n1, n2 in combinations(data, 2):
        if n1 + n2 == 2020:
            print(n1 * n2)

    for n1, n2, n3 in combinations(data, 3):
        if n1 + n2 + n3 == 2020:
            print(n1 * n2 * n3)
