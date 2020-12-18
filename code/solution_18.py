from pathlib import Path
import re
from typing import List


DATA_PATH = Path(__file__).resolve().parents[1] / "data"


def read_input(path: Path) -> List[str]:
    return path.read_text().strip("\n").replace(" ", "").split("\n")


def evaluate_inner_expression_1(expression: str) -> int:
    """
    Solve a mathematical expression from left to right.
    Input must not contain parenthesis.
    """
    while "+" in expression or "*" in expression:
        expression = re.sub(
            r"(\d+[\+\*]\d+)",
            lambda x: str(eval(x.group(0))),
            expression,
            count=1,
        )
    return eval(expression)


def evaluate_inner_expression_2(expression: str) -> int:
    """
    Solve a mathematical expression by computing the addition,
    and then the multiplication. Input must not contain parenthesis.
    """
    while "+" in expression:
        expression = re.sub(
            r"(\d+\+\d+)",
            lambda x: str(eval(x.group(0))),
            expression,
            count=1,
        )
    return eval(expression)


def evaluate(expression: str, evaluation_function) -> int:
    """
    Solve a mathematical expression, using the evaluation_function to evaluate
    the expression without parenthesis.
    """
    while "(" in expression:
        # Find the inner parenthesis a compute its value
        expression = re.sub(
            r"(\([\d+\+\*]+\))",
            lambda x: str(evaluation_function(x.group(0)[1:-1])),
            expression,
        )

    return evaluation_function(expression)


def main(problem_number: int):
    data = read_input(DATA_PATH / f"input_{problem_number}.txt")

    # Part 1
    print(sum(evaluate(line, evaluate_inner_expression_1) for line in data))

    # Part 2
    print(sum(evaluate(line, evaluate_inner_expression_2) for line in data))
