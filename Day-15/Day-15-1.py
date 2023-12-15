import sys
from argparse import ArgumentParser
import logging
from pprint import pprint
from os.path import basename
from functools import reduce

from aocd.models import Puzzle


input1 = """"""

input2 = """"""


def _setup() -> tuple[Puzzle, str]:
    parser = ArgumentParser()
    parser.add_argument("-e", "--example", default=None)
    args = parser.parse_args()
    problem_day = int(basename(sys.argv[0]).split("-")[1])
    puzzle = Puzzle(2023, problem_day)
    if args.example is not None:
        logging.getLogger().setLevel("DEBUG")
    return puzzle, args.example


def parse_input(input_string: str) -> list[str]:
    # print(input_string)
    input_list = input_string.split(",")
    return input_list


def aoc_hash(input_step: str) -> int:
    return reduce(
        lambda acc, next_char: ((acc+ord(next_char))*17) % 256,
        input_step,
        0
    )


def _solve(input_string: str) -> int:
    input_list = parse_input(input_string)
    for step in input_list:
        print(step, aoc_hash(step))
    return sum([aoc_hash(step) for step in input_list])


def _main():
    puzzle, do_example = _setup()
    if do_example:
        answer = _solve(puzzle.examples[0].input_data)
        logging.debug(f"example result = {puzzle.examples[0].answer_a}")
    else:
        answer = _solve(puzzle.input_data)
    print(f"answer = {answer}")


if __name__ == "__main__":
    _main()
