from argparse import ArgumentParser
import logging
from pprint import pprint
from math import prod

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


def parse_input(input_string: str) -> list[tuple[int, int]]:
    input_lines = input_string.splitlines()
    times = [
        int(t)
        for t in input_lines[0].split(":")[1].split()
    ]
    distances = [
        int(d)
        for d in input_lines[1].split(":")[1].split()
    ]
    return list(
        zip(times, distances)
    )


def optimize_race(milliseconds: int, distance: int) -> int:

    # forward
    for forward_time in range(milliseconds//2):
        speed = forward_time
        travel_time = milliseconds - forward_time
        forward_distance = speed * travel_time
        if forward_distance > distance:
            break

    for backward_time in range(milliseconds, milliseconds//2, -1):
        speed = milliseconds - backward_time
        travel_time = backward_time
        backward_distance = speed * travel_time
        if backward_distance > distance:
            break

    print(milliseconds, forward_time, backward_time, backward_time - forward_time + 1)

    return backward_time - forward_time + 1


def _solve(input_string: str) -> int:

    races_list = parse_input(input_string)

    result = prod([
        optimize_race(*one_race)
        for one_race in races_list
    ])

    return result



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
