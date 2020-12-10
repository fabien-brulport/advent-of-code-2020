from collections import deque
from itertools import combinations
from pathlib import Path
from typing import List


DATA_PATH = Path(__file__).resolve().parents[1] / "data"


def read_input(path: Path) -> List[int]:
    data = path.read_text().strip("\n").split("\n")
    return [int(line) for line in data]


def is_valid(element: int, queue: List[int]) -> bool:
    """
    Return True if the element is valid with respect
    to the queue (if the sum of 2 elements of the queue
    is equal to the element).
    """
    for el1, el2 in combinations(queue, 2):
        if el1 + el2 == element:
            return True
    return False


def get_first_invalid_element(data: List[int], queue_size: int = 25) -> int:
    queue = deque(data[:queue_size], queue_size)

    for element in data[queue_size:]:
        if not is_valid(element, queue):
            return element

        queue.append(element)

    raise RuntimeError("No invalid number found")


def get_contiguous_set(data: List[int], invalid_element: int) -> List[int]:
    for set_length in range(2, len(data)):
        number_of_possible_set = len(data) - set_length + 1
        for start_index in range(number_of_possible_set):
            current_set = data[start_index : start_index + set_length]
            if sum(current_set) == invalid_element:
                return current_set

    raise RuntimeError("No contiguous set found")


def main(problem_number: int):
    data = read_input(DATA_PATH / f"input_{problem_number}.txt")
    # Part 1
    invalid_element = get_first_invalid_element(data)
    print(invalid_element)

    # Part 2
    contiguous_set = get_contiguous_set(data, invalid_element)
    print(min(contiguous_set) + max(contiguous_set))
