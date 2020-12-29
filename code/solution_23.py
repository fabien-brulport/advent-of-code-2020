from pathlib import Path
from typing import List, Dict


DATA_PATH = Path(__file__).resolve().parents[1] / "data"


def read_input(path: Path) -> List[int]:
    return list(map(int, path.read_text().strip("\n")))


def play_one_round(
    linked_list: Dict[int, int], current_cup: int, max_value: int
) -> int:
    """
    Update the linked list by playing one round: select the 3 cups after
    the current_cup, move it behind the destination cup, and return the next
    cup.
    """
    # The 3 elements that are moved
    n1 = linked_list[current_cup]
    n2 = linked_list[n1]
    n3 = linked_list[n2]

    # Find destination number
    destination = current_cup
    destination = (destination - 2) % max_value + 1
    while (destination == n1) or (destination == n2) or (destination == n3):
        destination = (destination - 2) % max_value + 1

    # Next cup
    next_cup = linked_list[n3]

    # Update the linked list at once
    linked_list[current_cup], linked_list[n3], linked_list[destination] = (
        next_cup,
        linked_list[destination],
        n1,
    )

    return next_cup


def main(problem_number: int):
    # Part 1
    data = read_input(DATA_PATH / f"input_{problem_number}.txt")
    linked_list = {k: v for k, v in zip(data[:-1], data[1:])}
    linked_list[data[-1]] = data[0]

    # Play 100 rounds
    value = data[0]
    for _ in range(100):
        value = play_one_round(linked_list, value, max(data))

    # Build the result: the cups that follow the cup 1
    result = []
    cup = 1
    for _ in range(len(linked_list) - 1):
        cup = linked_list[cup]
        result.append(cup)
    print("".join(map(str, result)))

    # Part 2
    linked_list = {k: v for k, v in zip(data[:-1], data[1:])}
    n_cups = 1_000_000
    n_rounds = 10_000_000

    # Complete the linled_list to get a length of n_cups
    key = data[-1]
    for i in range(max(data) + 1, n_cups + 1):
        linked_list[key] = i
        key = i
    linked_list[key] = data[0]

    # Play 10 000 000 rounds
    value = data[0]
    for _ in range(n_rounds):
        value = play_one_round(linked_list, value, n_cups)

    print(linked_list[1] * linked_list[linked_list[1]])
