from dataclasses import dataclass
from pathlib import Path
import re
from typing import Dict, List, Tuple


DATA_PATH = Path(__file__).resolve().parents[1] / "data"


@dataclass
class Bag:
    """
    A Bag is a node of the graph, both the children and the parents
    are added when parsing the rules, because the parents are useful for
    part 1 and the children for part 2.
    """

    name: str
    children: List[Tuple[str, int]]
    parents: List[str]


def read_input(path: Path) -> Dict[str, Bag]:
    data = path.read_text().strip("\n").split("\n")
    bags = dict()
    for line in data:
        container_bag_name = re.match("^(?P<name>.*) bags contain", line).group("name")
        container_bag = bags.setdefault(
            container_bag_name, Bag(container_bag_name, [], [])
        )
        bags_contained_name = re.findall(r"(\d) ([a-z]+ [a-z]+)", line)
        for number, bag_name in bags_contained_name:
            contained_bag = bags.setdefault(bag_name, Bag(bag_name, [], []))
            # Add the container name to the parents of the contained bag
            contained_bag.parents.append(container_bag)
            # Add how many bags of each type are contained in the container
            container_bag.children.append((bag_name, int(number)))

    return bags


def main(problem_number: int):
    data = read_input(DATA_PATH / f"input_{problem_number}.txt")
    # Part 1
    node_to_visit = ["shiny gold"]
    node_visited = []
    result = set()
    while node_to_visit:
        bag = data[node_to_visit.pop(0)]
        for parent in bag.parents:
            result.add(parent.name)
            if parent.name not in node_visited:
                node_to_visit.append(parent.name)
        node_visited.append(bag.name)

    print(len(result))

    # Part 2
    node_to_visit = [("shiny gold", 1)]
    result = 0
    while node_to_visit:
        bag_name, bag_number = node_to_visit.pop(0)
        bag = data[bag_name]
        result += bag_number
        for children_name, children_number in bag.children:
            node_to_visit.append((children_name, children_number * bag_number))

    # Removing 1 to remove the shiny gold bag
    print(result - 1)
