from argparse import ArgumentParser
import logging
from pprint import pprint
from itertools import cycle

from aocd.models import Puzzle


def _setup() -> tuple[Puzzle, str]:
    parser = ArgumentParser()
    parser.add_argument("-e", "--example", default=None)
    parser.add_argument("day_number", type=int)
    args = parser.parse_args()
    puzzle = Puzzle(2023, args.day_number)
    if args.example is not None:
        logging.getLogger().setLevel("DEBUG")
    return puzzle, args.example


def parse_input(input_string: str) -> tuple[str, dict]:
    input_lines = input_string.splitlines()

    directions = input_lines[0]

    maps = {}
    for one_map in input_lines[2:]:
        maps[one_map[0:3]] = {
            "L": one_map[7:10],
            "R": one_map[12:15]
        }

    return directions, maps


def _solve(input_string: str) -> int:
    directions, maps = parse_input(input_string)
    print(directions)
    pprint(maps)
    current_location = "AAA"
    number_of_steps = 0
    for one_step in cycle(directions):
        current_location = maps[current_location][one_step]
        number_of_steps += 1
        if number_of_steps % 100 == 0:
            print(number_of_steps)
        if current_location == "ZZZ":
            break

    return number_of_steps


def _main():
    puzzle, do_example = _setup()
    if do_example:
        # answer = _solve(puzzle.examples[0].input_data)
        answer = _solve("""LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
""")
        logging.debug(f"example result = {puzzle.examples[0].answer_a}")
    else:
        answer = _solve(puzzle.input_data)
    print(f"answer = {answer}")


if __name__ == "__main__":
    _main()
