from argparse import ArgumentParser
import logging
from pprint import pprint
from itertools import pairwise

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


def parse_input(input_string: str) -> list[list[int]]:
    return [
        [
            int(element)
            for element in one_line.split()
        ]
        for one_line in input_string.splitlines()
    ]


def solve_one_sequence(sequence: list[int]) -> int:
    solution_array = [sequence]
    working_sequence = sequence
    while True:
        deltas = [
            x_n_plus_one - x_n
            for x_n, x_n_plus_one in pairwise(working_sequence)
        ]
        if sum([abs(x) for x in deltas]) == 0:
            break
        else:
            solution_array.append(deltas)
            working_sequence = deltas

    # pprint(solution_array)

    result = 0
    for sequence_n_plus_one, sequence_n in pairwise(reversed(solution_array)):
        sequence_n.append(sequence_n[-1]+sequence_n_plus_one[-1])
        print(sequence_n_plus_one, sequence_n)
        result = sequence_n[-1]

    return result


def _solve(input_string: str) -> int:
    inputs_list = parse_input(input_string)
    # pprint(inputs_list)
    # print(max([len(x) for x in inputs_list]))
    return sum([
        solve_one_sequence(one_sequence)
        for one_sequence in inputs_list
    ])


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
