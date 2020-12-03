from functools import reduce
import operator
from pathlib import Path
from typing import List

import numpy as np


DATA_PATH = Path(__file__).resolve().parents[1] / "data"


def read_input(path: Path) -> np.ndarray:
    data = path.read_text().strip("\n").split("\n")
    return np.array([list(line) for line in data])


def compute_n_trees(grid: np.ndarray, delta_x: int, delta_y: int) -> int:
    position_x, position_y = 0, 0
    n_trees = 0
    while True:
        position_x, position_y = (position_x + delta_x) % grid.shape[
            1
        ], position_y + delta_y
        if position_y >= len(grid):
            return n_trees
        if grid[position_y, position_x] == "#":
            n_trees += 1


def main(problem_number: int):
    grid = read_input(DATA_PATH / f"input_{problem_number}.txt")

    # Part 1
    slope = (3, 1)
    print(compute_n_trees(grid, *slope))

    # Part 2
    slopes = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    ]
    print(reduce(operator.mul, (compute_n_trees(grid, *slope) for slope in slopes), 1))
