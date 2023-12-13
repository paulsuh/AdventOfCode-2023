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

dead_patterns = []


def _setup() -> tuple[Puzzle, str]:
    parser = ArgumentParser()
    parser.add_argument("-e", "--example", default=None)
    parser.add_argument("day_number", type=int)
    args = parser.parse_args()
    puzzle = Puzzle(2023, args.day_number)
    if args.example is not None:
        logging.getLogger().setLevel("DEBUG")
    return puzzle, args.example


def parse_input(input_string: str) -> list[list[list[str]]]:
    # print(input_string)
    result = []
    one_pattern = []
    for one_line in input_string.splitlines():
        if len(one_line) == 0:
            result.append(one_pattern)
            one_pattern = []
        else:
            one_pattern.append(list(one_line))
    result.append(one_pattern)
    return result


def check_one_reflection(chunk1: Iterator, chunk2: Iterator) -> bool:
    for line1, line2 in zip(chunk1, chunk2):
        if line1 != line2:
            return False
    return True


def check_horizontal_reflection(pattern: list[list[str]] | list[tuple[str]], ignore_index: int) -> int:
    for line_num in range(1, len(pattern)):
        if line_num == ignore_index:
            continue
        chunk1 = reversed(pattern[:line_num])
        chunk2 = iter(pattern[line_num:])
        if check_one_reflection(chunk1, chunk2):
            return line_num

    return 0


def check_vertical_reflection(pattern: list[list[str]], ignore_index: int) -> int:
    transposed_pattern = transpose(pattern)
    result = check_horizontal_reflection(list(transposed_pattern), ignore_index)
    return result


def solve_for_smudges(pattern: list[list[str]]) -> int:

    # first get the "no smudge" values - these should be ignored
    no_smudge_horizontal = check_horizontal_reflection(pattern, 0)
    no_smudge_vertical = check_vertical_reflection(pattern, 0)

    for row_num in range(len(pattern)):
        for col_num in range(len(pattern[0])):
            # flip the cell
            pattern[row_num][col_num] = "#" if pattern[row_num][col_num] == "." else "."
            if (result := check_horizontal_reflection(pattern, no_smudge_horizontal)) > 0:
                if result != no_smudge_horizontal:
                    return result*100
            if (result := check_vertical_reflection(pattern, no_smudge_vertical)) > 0:
                if result != no_smudge_vertical:
                    return result
            # flip the cell back before trying the next cell
            pattern[row_num][col_num] = "#" if pattern[row_num][col_num] == "." else "."

    return 0



def _solve(input_string: str) -> int:
    input_list = parse_input(input_string)
    # pprint(input_list, width=120)
    return sum([
        solve_for_smudges(one_pattern)
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
