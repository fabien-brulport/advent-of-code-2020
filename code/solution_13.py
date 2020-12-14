from functools import reduce
import operator
from pathlib import Path
from typing import List, Union, Tuple


DATA_PATH = Path(__file__).resolve().parents[1] / "data"


def read_input(path: Path) -> Tuple[int, List[Union[str, int]]]:
    time_stamp, buses = path.read_text().strip("\n").split("\n")
    buses = [bus if bus == "x" else int(bus) for bus in buses.split(",")]
    return int(time_stamp), buses


def get_min_start_time(time_stamp: int, buses: List[int]) -> Tuple[int, int]:
    time_to_wait_min = time_stamp
    bus_id_min = -1
    for bus_id in buses:
        time_since_last_depart = time_stamp % bus_id
        if time_since_last_depart == 0:
            return bus_id, 0
        time_to_wait = bus_id - time_since_last_depart
        if time_to_wait < time_to_wait_min:
            time_to_wait_min = time_to_wait
            bus_id_min = bus_id
    return bus_id_min, time_to_wait_min


def extended_euclidean(a: int, b: int) -> Tuple[int, int, int]:
    """
    Return (r, u, v) such that a*u + b*v = r = gcd(a, b).

    From https://fr.wikipedia.org/wiki/Algorithme_d%27Euclide_%C3%A9tendu
    """

    r, u, v, r_prime, u_prime, v_prime = a, 1, 0, b, 0, 1

    while r_prime != 0:
        q = r // r_prime
        r, u, v, r_prime, u_prime, v_prime = (
            r_prime,
            u_prime,
            v_prime,
            r - q * r_prime,
            u - q * u_prime,
            v - q * v_prime,
        )

    return r, u, v


def solve_chinese_remainder(a_list: List[int], n_list: List[int]):
    """
    From https://fr.wikipedia.org/wiki/Th%C3%A9or%C3%A8me_des_restes_chinois
    """
    n_prod = reduce(operator.mul, n_list, 1)

    res = 0
    for n_i, a_i in zip(n_list, a_list):
        n_hat_i = n_prod // n_i
        *_, v = extended_euclidean(n_i, n_hat_i)
        res += v * n_hat_i * a_i

    return res % n_prod


def main(problem_number: int):
    time_stamp, buses = read_input(DATA_PATH / f"input_{problem_number}.txt")
    # Part 1
    filtered_buses = [bus_id for bus_id in buses if bus_id != "x"]
    bus_id, time_to_wait = get_min_start_time(time_stamp, filtered_buses)
    print(bus_id * time_to_wait)

    # Part 2
    deltas = []
    buses_id = []
    for delta, bus_id in enumerate(buses):
        if bus_id == "x":
            continue
        deltas.append(delta)
        buses_id.append(bus_id)

    max_delta = max(deltas)
    # Reverse the delta to get the
    a_list = [max_delta - d for d in deltas]
    res = solve_chinese_remainder(a_list, buses_id)
    print(res - max_delta)
