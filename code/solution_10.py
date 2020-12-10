from functools import reduce
from collections import Counter
import operator
from pathlib import Path
from typing import List


DATA_PATH = Path(__file__).resolve().parents[1] / "data"


def read_input(path: Path) -> List[int]:
    data = path.read_text().strip("\n").split("\n")
    return [int(line) for line in data]


def count_diff(sorted_jolts: List[int]) -> Counter:
    """
    Compute all the gap between sorted values, and returns the count
    of each diff for the different values.
    """
    all_diffs = []
    for lower_jolt, upper_jolt in zip(sorted_jolts[:-1], sorted_jolts[1:]):
        all_diffs.append(upper_jolt - lower_jolt)
    return Counter(all_diffs)


def count_contiguous_sets_length(sorted_jolts: List[int]) -> Counter:
    """
    Find the contiguous sets in the sorted list: a contiguous set
    is a set of value in which all diff between the value is 1.
    Then the function return a Counter where the key is the length
    of the sets, and the value the number of sets with this length
    in the input.
    """
    sets_length = list()
    len_current_set = 1
    for lower_jolt, upper_jolt in zip(sorted_jolts[:-1], sorted_jolts[1:]):
        if upper_jolt - lower_jolt == 1:
            len_current_set += 1
        elif upper_jolt - lower_jolt == 3:
            sets_length.append(len_current_set)
            len_current_set = 1

    results = Counter(sets_length)
    return results


def main(problem_number: int):
    data = read_input(DATA_PATH / f"input_{problem_number}.txt")
    jolts = list(data)
    jolts.append(0)  # outlet
    jolts.append(max(data) + 3)  # device
    sorted_jolts = sorted(jolts)

    # Part 1
    diff_counter = count_diff(sorted_jolts)
    print(diff_counter[1] * diff_counter[3])

    # Part 2
    sets_length_counter = count_contiguous_sets_length(sorted_jolts)
    # I did this dict by hand, could be nice to have it programatically
    n_permutation_for_set_size = {
        1: 1,
        2: 1,
        3: 2,
        4: 4,
        5: 7,
    }
    possibilities = [
        n_permutation_for_set_size[value] ** number
        for value, number in sets_length_counter.items()
    ]

    print(reduce(operator.mul, possibilities, 1))
