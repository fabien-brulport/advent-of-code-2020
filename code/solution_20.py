from dataclasses import dataclass
from pathlib import Path
import re
from typing import List, Optional, Tuple
import operator
from functools import reduce


DATA_PATH = Path(__file__).resolve().parents[1] / "data"


@dataclass
class Tile:
    number: int
    array: List[List[int]]
    neighboors: Optional[List["Tile"]] = None

    def borders(self):
        """Order: top, right, bottom, left"""
        yield self.array[0]
        yield [line[-1] for line in self.array]
        yield self.array[-1]
        yield [line[0] for line in self.array]

    def is_neighboor(self, other: "Tile") -> bool:
        if self.number == other.number:
            return False
        for border in self.borders():
            for other_border in other.borders():
                # Sanity check
                if sum(border) != sum(other_border):
                    continue
                if border == other_border or border == other_border[::-1]:
                    return True

        return False

    def matching_border(self, other: "Tile") -> Tuple[int, int, bool]:
        for idx, border in enumerate(self.borders()):
            for idx_other, other_border in enumerate(other.borders()):
                if border == other_border:
                    return idx, idx_other, False
                if border == other_border[::-1]:
                    return idx, idx_other, True

        raise ValueError("The tiles are not neighboors")

    def flip(self, axis: int):
        if axis == 0:
            self.array = self.array[::-1]
        elif axis == 1:
            self.array = [line[::-1] for line in self.array]
        else:
            raise ValueError(f"Axis : {axis}")

    def rotate(self):
        new_array = []
        for idx in reversed(range(len(self.array[0]))):
            new_array.append([line[idx] for line in self.array])
        self.array = new_array


def assemble_puzzle(tiles: List[Tile], first_tile: Tile):
    tiles_done = set()

    # Set correct first corner
    indexes = [first_tile.matching_border(n)[0] for n in first_tile.neighboors]
    for _ in range((min(indexes) - 1) % 4):
        first_tile.rotate()
    # tiles_done.add(first_tile.number)
    tiles_to_do = [first_tile]
    while tiles_to_do:
        tile = tiles_to_do.pop(0)
        for n in tile.neighboors:
            if n.number in tiles_done:
                continue
            idx, idx_other, reverse = tile.matching_border(n)
            for i in range((idx_other - (idx - 2)) % 4):
                n.rotate()
                idx, idx_other, reverse = tile.matching_border(n)

            print(idx, idx_other)
            assert idx == 1 or idx == 2, idx
            if reverse:
                n.flip((idx_other - 1) % 2)
            if n.number not in tiles_done:
                tiles_to_do.append(n)

        tiles_done.add(n.number)


def read_input(path: Path) -> List[int]:
    tiles = []
    for tile in path.read_text().strip("\n").split("\n\n"):
        number = re.match(r"Tile (?P<number>\d+):", tile).group("number")
        array = []
        for line in tile.split("\n")[1:]:
            array.append([1 if char == "#" else 0 for char in line])

        tiles.append(Tile(int(number), array))

    return tiles


def main(problem_number: int):
    tiles = read_input(DATA_PATH / f"input_{problem_number}.txt")
    # Part 1
    corners = []
    for tile in tiles:
        neighboors = []
        for other_tile in tiles:
            if tile.is_neighboor(other_tile):
                neighboors.append(other_tile)
        tile.neighboors = neighboors

        if len(neighboors) == 2:
            corners.append(tile)

    print(reduce(operator.mul, (corner.number for corner in corners)))

    # Part 2
    assemble_puzzle(tiles, corners[0])
