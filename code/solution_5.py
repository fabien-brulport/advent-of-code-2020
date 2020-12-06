from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple


DATA_PATH = Path(__file__).resolve().parents[1] / "data"


@dataclass
class BoardingPass:
    row_characters: str
    col_characters: str

    @classmethod
    def from_str(cls, line: str) -> "BoardingPass":
        return cls(row_characters=line[:7], col_characters=line[7:])

    @staticmethod
    def _get_index(characters: str, upper_char: str) -> int:
        len_part = 2 ** len(characters)
        lower_idx = 0
        for char in characters:
            len_part /= 2
            if char == upper_char:
                lower_idx += len_part
        return int(lower_idx)
 

    def get_position(self) -> Tuple[int, int]:
        return (self._get_index(self.row_characters, "B"), 
        self._get_index(self.col_characters, "R"))

    def get_seat_id(self) -> int:
        row, col = self.get_position()
        return row * 8 + col
           


def read_input(path: Path) -> List[BoardingPass]:
    lines = path.read_text().strip("\n").split("\n")
    return [BoardingPass.from_str(line) for line in lines]

def main(problem_number: int):
    data = read_input(DATA_PATH / f"input_{problem_number}.txt")
    all_seat_ids = [boardingpass.get_seat_id() for boardingpass in data]
    print(max(all_seat_ids))

    all_seat_ids = sorted(all_seat_ids)
    for seat_id, seat_id_next in zip(all_seat_ids[:-1], all_seat_ids[1:]):
        if seat_id_next - seat_id != 1:
            print(seat_id + 1)


