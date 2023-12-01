from argparse import ArgumentParser
import logging

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


def _solve(input: str):
    result = 0
    for one_line in input.splitlines():
        line_digits = [
            c
            for c in one_line
            if c.isdigit()
        ]
        logging.debug(f"{line_digits[0]+line_digits[-1]}")
        result += int(line_digits[0]+line_digits[-1])

    return result


def _main():
    puzzle, do_example = _setup()
    if do_example:
        answer = _solve(puzzle.examples[0].input_data)
    else:
        answer = _solve(puzzle.input_data)

    print(answer)


if (__name__ == "__main__"):
    _main()
