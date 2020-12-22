from pathlib import Path
import re
from typing import List, Tuple, Dict

import regex


DATA_PATH = Path(__file__).resolve().parents[1] / "data"


def read_input(path: Path) -> Tuple[Dict[int, str], List[str]]:
    blocks = path.read_text().strip("\n").split("\n\n")
    messages = blocks[1].split("\n")
    rules = dict()
    for line in blocks[0].split("\n"):
        number, rule = line.split(": ")
        if '"' in rule:
            rule = rule.replace('"', "")
        else:
            rule = f"({rule})"
            rule = rule.replace("|", ")|(")
            rule = re.sub(r"\d+", lambda x: f"({x.group(0)})", rule)
            rule = rule.replace(" ", "")

        rules[int(number)] = rule
    return rules, messages


def evaluate_rule_part_1(rules: Dict[int, str], number: int = 0) -> str:
    """Evaluate the rules recursively: replace (1) by the rule 1 for instance"""
    string = re.sub(
        r"(\d+)", lambda x: evaluate_rule_part_1(rules, int(x.group(0))), rules[number]
    )
    rules[number] = string
    return string


def evaluate_rule_part_2(rules: Dict[int, str], number: int = 0) -> str:
    """Same as evaluate_rule_part_1 but add recursion for rule 8 and 11"""
    if number == 8:
        string = f"(?P<rule8>({evaluate_rule_part_2(rules, 42)})(?&rule8)?)"
    elif number == 11:
        string = (
            f"(?P<rule11>({evaluate_rule_part_2(rules, 42)})(?&rule11)?"
            f"({evaluate_rule_part_2(rules, 31)}))"
        )
    else:
        string = re.sub(
            r"(\d+)",
            lambda x: evaluate_rule_part_2(rules, int(x.group(0))),
            rules[number],
        )
    rules[number] = string
    return string


def main(problem_number: int):
    # Part 1
    rules, messages = read_input(DATA_PATH / f"input_{problem_number}.txt")
    evaluate_rule_part_1(rules)
    print(sum(1 for message in messages if re.fullmatch(rules[0], message) is not None))

    # Part 2
    rules, messages = read_input(DATA_PATH / f"input_{problem_number}.txt")
    evaluate_rule_part_2(rules)
    # Recursion is not implemented in the re package, regex is needed
    print(
        sum(1 for message in messages if regex.fullmatch(rules[0], message) is not None)
    )
