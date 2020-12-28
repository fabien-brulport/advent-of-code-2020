from pathlib import Path
from typing import List


DATA_PATH = Path(__file__).resolve().parents[1] / "data"


def read_input(path: Path) -> List[int]:
    # return list(map(int, "389125467".strip("\n")))
    return list(map(int, path.read_text().strip("\n")))


def play_one_round(data: List[int], max_value: int):
    current_value = data.pop(0)
    data.append(current_value)
    n1 = data.pop(0)
    n2 = data.pop(0)
    n3 = data.pop(0)

    current_value = (current_value - 2) % max_value + 1
    while (current_value == n1) or (current_value == n2) or (current_value == n3):
        current_value = (current_value - 2) % max_value + 1

    idx = data.index(current_value)
    print(idx, current_value)
    data[idx + 1 : idx + 1] = [n1, n2, n3]


def main(problem_number: int):
    # Part 1
    data = read_input(DATA_PATH / f"input_{problem_number}.txt")
    for _ in range(100):
        play_one_round(data, 9)
        print(data)
    index_1 = data.index(1)
    print("".join(map(str, (data[index_1:] + data[:index_1])[1:])))

    # # Part 2
    # data = read_input(DATA_PATH / f"input_{problem_number}.txt")
    # n_cups = 1_000_000
    # n_rounds = 100_000
    # for i in range(max(data) + 1, n_cups + 1):
    #     data.append(i)
    # for _ in range(n_rounds):
    #     play_one_round(data, n_cups)
    # index_1 = data.index(1)
    # print(index_1)
    # print(data[index_1 - 10 : index_1 + 10])
    # print(data[: index_1 + 10])
    # print(data[(index_1 + 1) % len(data)] * data[(index_1 + 2) % len(data)])
