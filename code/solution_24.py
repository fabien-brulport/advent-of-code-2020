import math
from pathlib import Path
from typing import List, Tuple, Set

VERTICAL_DELTA = round(math.sin(math.pi / 3), 3)

DATA_PATH = Path(__file__).resolve().parents[1] / "data"


DIRECTION_CONVERSION = {
    "ne": (0.5, VERTICAL_DELTA),
    "e": (1, 0),
    "se": (0.5, -VERTICAL_DELTA),
    "sw": (-0.5, -VERTICAL_DELTA),
    "w": (-1, 0),
    "nw": (-0.5, VERTICAL_DELTA),
}


def read_input(path: Path) -> List[int]:
    trajectory_list = []
    for line in path.read_text().strip("\n").split("\n"):
        trajectory = []
        line = list(line)
        while line:
            elem = line.pop(0)
            if elem == "s" or elem == "n":
                trajectory.append(elem + line.pop(0))
            else:
                trajectory.append(elem)

        trajectory_list.append(trajectory)

    return trajectory_list


def str_direction_to_delta(direction: str) -> Tuple[float, float]:
    return DIRECTION_CONVERSION[direction]


def neighboors(position: Tuple[float, float]):
    x, y = position
    for delta_x, delta_y in DIRECTION_CONVERSION.values():
        yield (round(x + delta_x, 3), round(y + delta_y, 3))


def simulate_one_day(black_tiles: Set[Tuple[int, int]]):
    white_tiles_done = set()
    tiles_to_remove = []
    tiles_to_add = []

    for black_tile in black_tiles:
        # Check if the black tile needs to be flipped
        n_neighboors_black = sum(p in black_tiles for p in neighboors(black_tile))
        if n_neighboors_black == 0 or n_neighboors_black > 2:
            tiles_to_remove.append(black_tile)

        # Check if its white neighboor tiles need to be flipped
        for neighboor in neighboors(black_tile):
            if neighboor in black_tiles or neighboor in white_tiles_done:
                continue
            n_neighboors_black = sum(p in black_tiles for p in neighboors(neighboor))
            if n_neighboors_black == 2:
                tiles_to_add.append(neighboor)
            white_tiles_done.add(neighboor)

    # Flip the tiles all at once
    for tile in tiles_to_remove:
        black_tiles.remove(tile)
    for tile in tiles_to_add:
        black_tiles.add(tile)


def main(problem_number: int):
    # Part 1
    trajectory_list = read_input(DATA_PATH / f"input_{problem_number}.txt")
    black_tiles = set()
    for trajectory in trajectory_list:
        x, y = 0, 0
        for direction in trajectory:
            delta_x, delta_y = str_direction_to_delta(direction)
            x += delta_x
            y += delta_y

        coord = (x, round(y, 3))
        if coord in black_tiles:
            black_tiles.remove(coord)
        else:
            black_tiles.add(coord)

    print(len(black_tiles))

    # Part 2
    for _ in range(100):
        simulate_one_day(black_tiles)
    print(len(black_tiles))
