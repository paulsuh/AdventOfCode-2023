from argparse import ArgumentParser
import logging
from pprint import pprint
from typing import Iterator
from more_itertools import transpose

from aocd.models import Puzzle


input1 = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""

input2 = """"""


def _setup() -> tuple[Puzzle, str]:
    parser = ArgumentParser()
    parser.add_argument("-e", "--example", default=None)
    parser.add_argument("day_number", type=int)
    args = parser.parse_args()
    puzzle = Puzzle(2023, args.day_number)
    if args.example is not None:
        logging.getLogger().setLevel("DEBUG")
    return puzzle, args.example


def parse_input(input_string: str) -> list[list[str]]:
    # print(input_string)
    result = []
    one_pattern = []
    for one_line in input_string.splitlines():
        if len(one_line) == 0:
            result.append(one_pattern)
            one_pattern = []
        else:
            one_pattern.append(one_line)
    result.append(one_pattern)
    return result


def check_one_reflection(chunk1: Iterator, chunk2: Iterator) -> bool:
    for line1, line2 in zip(chunk1, chunk2):
        if line1 != line2:
            return False
    return True


def check_horizontal_reflection(pattern: list[str]) -> int:
    for line_num in range(1, len(pattern)):
        chunk1 = reversed(pattern[:line_num])
        chunk2 = iter(pattern[line_num:])
        if check_one_reflection(chunk1, chunk2):
            return line_num

    return 0


def check_vertical_reflection(pattern: list[str]) -> int:
    transposed_pattern = transpose(pattern)
    result = check_horizontal_reflection(list(transposed_pattern))
    return result


def _solve(input_string: str) -> int:
    input_list = parse_input(input_string)
    # pprint(input_list)
    # print(check_horizontal_reflection(input_list[0]))
    # print(check_vertical_reflection(input_list[0]))
    return sum([
        check_horizontal_reflection(one_pattern)*100+check_vertical_reflection(one_pattern)
        for one_pattern in input_list
    ])


def _main():
    puzzle, do_example = _setup()
    if do_example:
        answer = _solve(input1)
        logging.debug(f"example result = {puzzle.examples[0].answer_a}")
    else:
        answer = _solve(puzzle.input_data)
    print(f"answer = {answer}")


if __name__ == "__main__":
    _main()
