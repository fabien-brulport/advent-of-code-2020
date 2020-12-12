from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import List


DATA_PATH = Path(__file__).resolve().parents[1] / "data"


def read_input(path: Path) -> List[int]:
    return list(map(list, path.read_text().strip("\n").split("\n")))


def get_visible_seat(
    grid: List[List[str]], row: int, col: int, distance_to_visible_seat: int
) -> List[str]:
    width = len(grid[0])
    height = len(grid)
    visible_seat = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue
            for distance in range(0, distance_to_visible_seat):
                distance += 1
                row_n = row + (i * distance)
                col_n = col + (j * distance)
                if not (0 <= row_n < height and 0 <= col_n < width):
                    break
                elem = grid[row_n][col_n]
                if elem != ".":
                    visible_seat.append(elem)
                    break

    return visible_seat


def update_grid(
    grid: List[List[str]], distance_to_visible_seat: int, n_seat_occupied: int
) -> bool:
    moves = []
    for row_index in range(len(grid)):
        for col_index in range(len(grid[0])):
            current_position = grid[row_index][col_index]
            if current_position == ".":
                continue
            elif current_position == "L":
                visible_seat = get_visible_seat(
                    grid, row_index, col_index, distance_to_visible_seat
                )
                if "#" not in visible_seat:
                    moves.append((row_index, col_index, "#"))

            elif current_position == "#":
                visible_seat = get_visible_seat(
                    grid, row_index, col_index, distance_to_visible_seat
                )
                counter = Counter(visible_seat)
                if counter["#"] >= n_seat_occupied:
                    moves.append((row_index, col_index, "L"))

    if not moves:
        return True

    for row_index, col_index, value in moves:
        grid[row_index][col_index] = value

    return False


def main(problem_number: int):
    grid = read_input(DATA_PATH / f"input_{problem_number}.txt")
    grid1 = deepcopy(grid)
    grid2 = deepcopy(grid)

    # Part 1
    terminated = False
    while not terminated:
        terminated = update_grid(grid1, distance_to_visible_seat=1, n_seat_occupied=4)

    print(Counter([element for line in grid1 for element in line])["#"])

    # Part 2
    terminated = False
    max_distance = max(len(grid2), len(grid2[0]))
    while not terminated:
        terminated = update_grid(
            grid2, distance_to_visible_seat=max_distance, n_seat_occupied=5
        )

    print(Counter([element for line in grid2 for element in line])["#"])
