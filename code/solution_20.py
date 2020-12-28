from dataclasses import dataclass
from functools import reduce
import math
import operator
from pathlib import Path
import re
from typing import List, Optional, Tuple


DATA_PATH = Path(__file__).resolve().parents[1] / "data"


@dataclass
class Tile:
    number: int
    array: List[List[int]]
    neighboors: Optional[List["Tile"]] = None
    position: Optional[Tuple[int, int]] = None

    def borders(self):
        """
        Return the border of the tile in this
        order: top, right, bottom, left.
        """
        yield self.array[0]
        yield [line[-1] for line in self.array]
        yield self.array[-1]
        yield [line[0] for line in self.array]

    def is_neighboor(self, other: "Tile") -> bool:
        """Return true if the other tile is a neighboor"""
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
        """
        For neightboor tiles, find which border matches and return the index
        for both tile (0 being top, etc. see the `borders` method)
        and if the other tile should be reversed.
        """

        for idx, border in enumerate(self.borders()):
            for idx_other, other_border in enumerate(other.borders()):
                if border == other_border:
                    return idx, idx_other, False
                if border == other_border[::-1]:
                    return idx, idx_other, True

        raise ValueError("The tiles are not neighboors")

    def flip(self, axis: int):
        """Flip the tile along the given axis."""
        self.array = flip(self.array, axis)

    def rotate(self):
        """Rotate the tile counter clockwise"""
        self.array = rotate(self.array)

    def __repr__(self):
        string = ""
        for line in self.array:
            string += f"{''.join('#' if elem else '.' for elem in line)}\n"
        return string


def flip(array, axis: int):
    """Flip the array along the given axis."""
    if axis == 0:
        return array[::-1]
    elif axis == 1:
        return [line[::-1] for line in array]
    else:
        raise ValueError(f"Axis : {axis}")


def rotate(array):
    """Rotate the array counter clockwise"""
    new_array = []
    for idx in reversed(range(len(array[0]))):
        new_array.append([line[idx] for line in array])
    return new_array


def assemble_puzzle(tiles: List[Tile], first_tile: Tile) -> List[List[int]]:
    """Assemble all the tiles in one image, starting from a corner."""
    tiles_done = set()

    # Set correct first corner
    indexes = [first_tile.matching_border(n)[0] for n in first_tile.neighboors]
    for _ in range((min(indexes) - 1) % 4):
        first_tile.rotate()

    tiles_to_do = [first_tile]
    first_tile.position = (0, 0)
    # Assign a position to each tile, and correct their orientation
    while tiles_to_do:
        tile = tiles_to_do.pop(0)
        for n in tile.neighboors:
            if n.number in tiles_done:
                continue
            idx, idx_other, reverse = tile.matching_border(n)
            for i in range((idx_other - (idx - 2)) % 4):
                n.rotate()
                idx, idx_other, reverse = tile.matching_border(n)

            if reverse:
                n.flip((idx_other - 1) % 2)

            row, col = tile.position
            if idx == 1:
                n.position = row, col + 1
            elif idx == 2:
                n.position = row + 1, col
            else:
                raise ValueError

            if n.number not in tiles_done and n not in tiles_to_do:
                tiles_to_do.append(n)

        tiles_done.add(tile.number)

    # Build image from all the tiles and positions
    n_tiles = int(math.sqrt(len(tiles)))
    tile_shape = len(tiles[0].array[0]) - 2
    image_size = n_tiles * tile_shape
    image = [[0 for _ in range(image_size)] for _ in range(image_size)]
    for tile in tiles:
        row, col = tile.position
        for i, line in enumerate(tile.array[1:-1]):
            image[row * tile_shape + i][
                col * tile_shape : (col + 1) * tile_shape
            ] = line[1:-1]

    return image


def extract_patch(image: List[List[int]], patch_size: Tuple[int, int]):
    """Generate all patches of size patch_size from the image."""
    patch_height, patch_width = patch_size
    image_height = len(image)
    image_width = len(image[0])
    for y in range(image_height - patch_height + 1):
        for x in range(image_width - patch_width + 1):
            patch = []
            for i in range(patch_height):
                patch.append(image[y + i][x : x + patch_width])
            yield patch


def patch_matches(monster: List[List[int]], patch: List[List[int]]) -> bool:
    """Return True if the patch matches the monster pattern."""
    for line_m, line_p in zip(monster, patch):
        for elem_m, elem_p in zip(line_m, line_p):
            if elem_m and not elem_p:
                return False

    return True


def generate_transformed_images(image: List[List[int]]):
    """
    Generate all the possible images (flipped, rotated).
    Some images returned may be duplicated.
    """
    yield image
    for _ in range(3):
        yield rotate(image)

    image_flipped = flip(image, axis=0)
    yield image_flipped
    for _ in range(3):
        yield rotate(image_flipped)
    image_flipped = flip(image, axis=1)
    yield image_flipped
    for _ in range(3):
        yield rotate(image_flipped)


def read_input(path: Path) -> List[int]:
    monster_raw = "                  # \n#    ##    ##    ###\n #  #  #  #  #  #   "
    monster = []
    for line in monster_raw.split("\n"):
        monster.append([1 if elem == "#" else 0 for elem in line])

    tiles = []
    for tile in path.read_text().strip("\n").split("\n\n"):
        number = re.match(r"Tile (?P<number>\d+):", tile).group("number")
        array = []
        for line in tile.split("\n")[1:]:
            array.append([1 if char == "#" else 0 for char in line])

        tiles.append(Tile(int(number), array))

    return tiles, monster


def main(problem_number: int):
    tiles, monster = read_input(DATA_PATH / f"input_{problem_number}.txt")
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
    image = assemble_puzzle(tiles, corners[0])

    patch_size = (len(monster), len(monster[0]))
    n_monsters = 0
    for transformed_image in generate_transformed_images(image):
        for patch in extract_patch(transformed_image, patch_size):
            if patch_matches(monster, patch):
                n_monsters += 1

    print(sum(sum(line) for line in image) - sum(sum(line) for line in monster) * 15)
