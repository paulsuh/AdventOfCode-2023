import sys
from argparse import ArgumentParser
import logging
from pprint import pprint
from os.path import basename
from functools import cache

from aocd.models import Puzzle

input1 = """"""

input2 = """"""


garden_map: list[str] | None = None
max_row: int = 0
max_col: int = 0


def _setup() -> tuple[Puzzle, str]:
    parser = ArgumentParser()
    parser.add_argument("-e", "--example", default=None)
    args = parser.parse_args()
    problem_day = int(basename(sys.argv[0]).split("-")[1])
    puzzle = Puzzle(2023, problem_day)
    if args.example is not None:
        logging.getLogger().setLevel("DEBUG")
    return puzzle, args.example


def parse_input(input_string: str) -> list[list[int]]:
    input_list = input_string.splitlines()
    return input_list


@cache
def find_open_plots_around_location(row: int, col: int) -> set[tuple[int, int]]:
    result_set = set()
    if row > 0 and garden_map[row-1][col] == ".":
        result_set.add((row-1, col))
    if col > 0 and garden_map[row][col-1] == ".":
        result_set.add((row, col-1))
    if row < max_row-1 and garden_map[row+1][col] == ".":
        result_set.add((row+1, col))
    if col < max_col-1 and garden_map[row][col+1] == ".":
        result_set.add((row, col+1))

    return result_set


def check_area_for_set(previous_plots: set[tuple[int, int]]) -> set[tuple[int, int]]:

    next_plots = set()
    for one_plot in previous_plots:
        next_plots |= find_open_plots_around_location(*one_plot)

    return next_plots


def _solve(input_string: str) -> int:
    global garden_map
    global max_row
    global max_col

    garden_map = parse_input(input_string)
    max_row = len(garden_map)
    max_col = len(garden_map[0])
    print(max_row, max_col)
    # pprint(garden_map)

    # locate the start, replace with "."
    for row_num, row_string in enumerate(garden_map):
        if (col_num := row_string.find("S")) > 0:
            plots_to_be_checked = {(row_num, col_num)}
            garden_map[row_num] = row_string.replace("S", ".")
            break

    print(plots_to_be_checked)

    for step_num in range(64):
        new_plots = check_area_for_set(plots_to_be_checked)
        # pprint(new_plots)
        print(step_num, len(new_plots))
        plots_to_be_checked = new_plots

    # pprint(plots_to_be_checked)
    print(find_open_plots_around_location.cache_info())
    return len(plots_to_be_checked)


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
