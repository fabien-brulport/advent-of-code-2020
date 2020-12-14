import itertools
from dataclasses import dataclass
from pathlib import Path
import re
from typing import List, Union, Tuple, Generator


DATA_PATH = Path(__file__).resolve().parents[1] / "data"
N_BITS = 36


@dataclass
class Instruction:
    address: int
    value: int
    mask: str

    @property
    def masked_value(self) -> int:
        """Return the value once the masked is applied (part 1)"""
        binary_value = format(self.value, f"0{N_BITS}b")
        assert len(binary_value) == len(self.mask)
        masked_binary_value = []
        for bv, m in zip(binary_value, self.mask):
            masked_binary_value.append(bv if m == "X" else m)
        return int("".join(masked_binary_value), 2)

    @property
    def masked_addresses(self) -> Generator[int, None, None]:
        """Yield all the addresses defined by the mask (part 2)"""
        binary_address = format(self.address, f"0{N_BITS}b")
        masked_binary_address = []
        floating_indexes = []
        for i, (ba, m) in enumerate(zip(binary_address, self.mask)):
            if m == "0":
                masked_binary_address.append(ba)
            elif m == "1":
                masked_binary_address.append("1")
            elif m == "X":
                floating_indexes.append(i)
                # the X will be replaced later
                masked_binary_address.append("X")
            else:
                raise ValueError

        for prod in itertools.product(["0", "1"], repeat=len(floating_indexes)):
            for elem, index in zip(prod, floating_indexes):
                masked_binary_address[index] = elem
            yield int("".join(masked_binary_address), 2)


def read_input(path: Path) -> Tuple[int, List[Union[str, int]]]:
    data = path.read_text().strip("\n").split("\n")
    program = []
    for line in data:
        if "mask" in line:
            current_mask = line[7:]
        else:
            match = re.search(r"^mem\[(?P<address>\d+)\] = (?P<value>\d+)$", line)
            program.append(
                Instruction(
                    address=int(match.group("address")),
                    value=int(match.group("value")),
                    mask=current_mask,
                )
            )

    return program


def main(problem_number: int):
    program = read_input(DATA_PATH / f"input_{problem_number}.txt")

    # Part 1
    memory = dict()
    for instruction in program:
        memory[instruction.address] = instruction.masked_value
    print(sum(memory.values()))

    # Part 2
    memory = dict()
    for instruction in program:
        for address in instruction.masked_addresses:
            memory[address] = instruction.value
    print(sum(memory.values()))
