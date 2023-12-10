from argparse import ArgumentParser
import logging
from pprint import pprint
from itertools import cycle
from functools import reduce
from math import lcm

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


def parse_input(input_string: str) -> tuple[str, dict[str, dict[str, str]]]:
    input_lines = input_string.splitlines()

    directions = input_lines[0]

    maps = {}
    for one_map in input_lines[2:]:
        maps[one_map[0:3]] = {
            "L": one_map[7:10],
            "R": one_map[12:15]
        }

    return directions, maps


def _solve_one(directions: str, maps: dict[str, dict[str, str]], start_string: str) -> int:
    current_location = start_string
    number_of_steps = 0
    for one_step in cycle(directions):
        current_location = maps[current_location][one_step]
        number_of_steps += 1
        if number_of_steps % 1000 == 0:
            print(number_of_steps)
        if current_location.endswith("Z"):
            break

    return number_of_steps


def _solve(input_string: str) -> int:
    directions, maps = parse_input(input_string)
    # print(directions)
    # pprint(maps)

    # x = _solve_one(directions, maps, "AAA")
    # find all of the nodes that start with "A"
    start_nodes = [
        node
        for node in maps.keys()
        if node.endswith("A")
    ]
    print(start_nodes)
    distances = [
        _solve_one(directions, maps, start_node)
        for start_node in start_nodes
    ]
    print(distances)
    result = lcm(*distances)

    return result


def _main():
    puzzle, do_example = _setup()
    if do_example:
        # answer = _solve(puzzle.examples[0].input_data)
        answer = _solve("""LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
""")
        logging.debug(f"example result = {puzzle.examples[0].answer_a}")
    else:
        answer = _solve(puzzle.input_data)
    print(f"answer = {answer}")


if __name__ == "__main__":
    _main()
