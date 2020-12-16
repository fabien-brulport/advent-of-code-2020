import operator
from functools import reduce
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Optional, Dict
import re


DATA_PATH = Path(__file__).resolve().parents[1] / "data"


@dataclass
class Rule:
    name: str
    ranges: List[Tuple[int, int]]

    @classmethod
    def from_str(cls, line: str) -> "Rule":
        pattern = (
            r"^(?P<name>.*): (?P<l_0>\d*)-(?P<u_0>\d*) or (?P<l_1>\d*)-(?P<u_1>\d*)$"
        )
        match = re.search(pattern, line)
        return Rule(
            match.group("name"),
            [
                (int(match.group("l_0")), int(match.group("u_0"))),
                (int(match.group("l_1")), int(match.group("u_1"))),
            ],
        )

    def invalid_number(self, number: int) -> bool:
        (l_0, u_0), (l_1, u_1) = self.ranges
        return not (l_0 <= number <= u_0 or l_1 <= number <= u_1)

    def __hash__(self):
        return hash(self.name)


def is_ticket_invalid(rules: List[Rule], ticket: List[int]) -> Optional[List[int]]:
    """
    Return None if the ticket is valid, else return the list of invalid
    numbers in the ticket.
    """
    invalid_numbers = []

    for number in ticket:
        if all(rule.invalid_number(number) for rule in rules):
            invalid_numbers.append(number)

    if invalid_numbers:
        return invalid_numbers


def is_rule_valid(rule: Rule, numbers: List[int]) -> bool:
    return all(not rule.invalid_number(number) for number in numbers)


def compute_rule_to_position_mapping(
    rules: List[Rule], tickets: List[List[int]]
) -> Dict[Rule, int]:
    """
    Map the rules to the positions (index).
    """
    # Build the assignement matrix which indicates which rule is valid for which indexes
    assignement_matrix = []
    n_associations = len(rules)
    for rule in rules:
        line = []
        for position in range(n_associations):
            line.append(is_rule_valid(rule, [ticket[position] for ticket in tickets]))
        assignement_matrix.append(line)

    rule_to_index = dict()
    for i in range(n_associations):
        valid_positions = [sum(line) for line in assignement_matrix]
        # Find the rule which has only one position matching
        rule_index = valid_positions.index(1)
        # Find the corresponding position
        position = assignement_matrix[rule_index].index(True)

        rule_to_index[rules[rule_index]] = position

        # Set both the row and the col to False, to ignore this
        # rule and this index in the next turn
        for line in assignement_matrix:
            line[position] = False
        assignement_matrix[rule_index] = [False] * n_associations

    return rule_to_index


def read_input(path: Path) -> List[int]:
    blocks = path.read_text().strip("\n").split("\n\n")
    rules = [Rule.from_str(line) for line in blocks[0].split("\n")]
    my_ticket = list(map(int, blocks[1].split("\n")[1].split(",")))
    nearby_tickets = [
        list(map(int, line.split(","))) for line in blocks[2].split("\n")[1:]
    ]
    return rules, my_ticket, nearby_tickets


def main(problem_number: int):
    rules, my_ticket, nearby_tickets = read_input(
        DATA_PATH / f"input_{problem_number}.txt"
    )

    # Part 1
    invalid_numbers = []
    valid_tickets = []
    for ticket in nearby_tickets:
        result = is_ticket_invalid(rules, ticket)
        if result is None:
            valid_tickets.append(ticket)
        else:
            invalid_numbers.extend(result)

    print(sum(invalid_numbers))

    # Part 2
    rule_to_index_mapping = compute_rule_to_position_mapping(rules, valid_tickets)
    my_departure_values = [
        my_ticket[idx]
        for rule, idx in rule_to_index_mapping.items()
        if rule.name.startswith("departure")
    ]
    print(reduce(operator.mul, my_departure_values))
