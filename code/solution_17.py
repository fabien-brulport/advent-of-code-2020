from itertools import product
from pathlib import Path
from typing import List, Tuple, Dict, Generator


DATA_PATH = Path(__file__).resolve().parents[1] / "data"


Grid = Dict[List[int], int]


def read_input(path: Path, dim: int) -> Grid:
    grid = dict()
    for y, line in enumerate(path.read_text().strip("\n").split("\n")):
        for x, element in enumerate(line):
            if element == "#":
                coord = (x, y) + tuple(0 for _ in range(dim - 2))
                grid[coord] = 1

    return grid


def neighboors(coord: List[int]) -> Generator[List[int], None, None]:
    """Yield the neighboors coordinates of this coord"""
    for delta_coord in product([-1, 0, 1], repeat=len(coord)):
        neighboor_coord = tuple(c + d_c for c, d_c in zip(coord, delta_coord))
        if neighboor_coord == coord:
            continue
        yield neighboor_coord


def compute_new_value(coord: List[int], grid) -> int:
    """
    Compute the new value of a point based on its neighboorhood"""
    value = grid.get(coord, 0)
    n_neighboors_active = sum(grid.get(neighboor, 0) for neighboor in neighboors(coord))
    if value and n_neighboors_active in [2, 3]:
        return 1
    if not value and n_neighboors_active == 3:
        return 1
    return 0


def extreme_value(grid) -> Generator[Tuple[int, int], None, None]:
    """Yield for each dimension, a tuple which contains the min and max index"""
    for coord_list in zip(*grid):
        yield min(coord_list), max(coord_list)


def generate_valid_coords(grid) -> Generator[List[int], None, None]:
    """Yield coords that should be evaluated in the current round."""
    range_generator = (
        range(v_min - 1, v_max + 2) for v_min, v_max in extreme_value(grid)
    )
    for coord in product(*range_generator):
        yield coord


def run_one_cycle(grid):
    # Store updates in a list to apply it once
    updates = []
    for coord in generate_valid_coords(grid):
        updates.append((coord, compute_new_value(coord, grid)))

    # Only keep the "1" in the dict, to avoid having a too long dict
    for coord, new_value in updates:
        if new_value:
            grid[coord] = new_value
        else:
            if coord in grid:
                del grid[coord]


def main(problem_number: int):
    # Part 1
    grid = read_input(DATA_PATH / f"input_{problem_number}.txt", dim=3)
    for i in range(6):
        run_one_cycle(grid)
    print(len(grid))

    # Part 2
    grid = read_input(DATA_PATH / f"input_{problem_number}.txt", dim=4)
    for i in range(6):
        run_one_cycle(grid)
    print(len(grid))
