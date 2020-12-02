import argparse
from importlib import import_module


def run_main(problem_number):
    module = import_module(f"code.solution_{problem_number}")
    module.main(problem_number)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("problem_number")
    args = parser.parse_args()
    run_main(args.problem_number)
