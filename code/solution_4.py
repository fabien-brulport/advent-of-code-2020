from dataclasses import dataclass
from pathlib import Path
import re
from typing import List


DATA_PATH = Path(__file__).resolve().parents[1] / "data"


@dataclass
class Passport:
    mapping: dict

    @classmethod
    def from_str(cls, line: str) -> "Passport":
        groups = re.split(r" |\n", line)
        d = dict(group.split(":") for group in groups)
        return cls(mapping=d)

    def has_all_keys(self) -> bool:
        # All key except cid
        required_keys = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
        return all(required_key in self.mapping for required_key in required_keys)

    def has_valid_values(self) -> bool:
        if not self.has_all_keys():
            return False
        constrains = {
            "byr": lambda byr: 1920 <= int(byr) <= 2002,
            "iyr": lambda iyr: 2010 <= int(iyr) <= 2020,
            "eyr": lambda eyr: 2020 <= int(eyr) <= 2030,
            "hgt": self.check_heigth,
            "hcl": lambda hcl: re.match(r"^#[\da-f]{6}$", hcl),
            "ecl": lambda ecl: re.match(r"^amb|blu|brn|gry|grn|hzl|oth$", ecl),
            "pid": lambda pid: re.match(r"^\d{9}$", pid),
            "cid": lambda _: True,
        }

        return all(
            constrains[key](value) for key, value in sorted(self.mapping.items())
        )

    @staticmethod
    def check_heigth(hgt: str) -> bool:
        res = re.match(r"^(\d+)(in|cm)$", hgt)
        if not res:
            return False
        number, unit = res.groups()
        if unit == "cm" and 150 <= int(number) <= 193:
            return True
        if unit == "in" and 59 <= int(number) <= 76:
            return True
        return False


def read_input(path: Path) -> List[Passport]:
    data = path.read_text().strip("\n").split("\n\n")
    return [Passport.from_str(line) for line in data]


def main(problem_number: int):
    data = read_input(DATA_PATH / f"input_{problem_number}.txt")

    # Part 1
    print(sum(passport.has_all_keys() for passport in data))
    # Part 2
    print(sum(passport.has_valid_values() for passport in data))
