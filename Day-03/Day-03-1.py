from argparse import ArgumentParser
import logging
from pprint import pprint
import re
from string import digits

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


adjacent_cells = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1)
]

expanded_input: list[str] = []


def expand_input(input: str) -> list[str]:
    # put a row of spaces before and after
    # put a space before and after each row
    # this lets us test adjacency without doing bounds checks
    result = [
        f".{one_line}."
        for one_line in input.splitlines()
    ]
    result.insert(0, "."*len(result[0]))
    result.append("."*len(result[0]))

    return result


def is_adjacent_to_symbol(row, col) -> bool:

    for row_delta, col_delta in adjacent_cells:
        if expanded_input[row+row_delta][col+col_delta] not in digits+".":
            return True

    # Never matched adjacent
    return False


def locate_numbers(row_num: int) -> list[int]:
    # scans a line to determine unitary numbers
    # return a list of numbers
    # first split line by digits
    result = []
    tmp_num = []
    is_adjacent = False
    for one_char, col in zip(expanded_input[row_num], range(len(expanded_input[row_num]))):
        if one_char.isdigit():
            # if it's a digit, add it to the temp number group
            tmp_num.append(one_char)
            is_adjacent |= is_adjacent_to_symbol(row_num, col)
        elif is_adjacent and len(tmp_num) > 0:
            # if it's not a digit, and we have accumulated a number
            # add it to the result and clear the accumulator
            result.append(int("".join(tmp_num)))
            tmp_num = []
            is_adjacent = False
        else:
            # it's not a digit and we have not accumulated a number
            # or the number is not adjacent
            tmp_num = []
            is_adjacent = False

    return result



def _solve(input):
    global expanded_input
    expanded_input = expand_input(input)
    nums_list = []
    for row in range(1, len(expanded_input)-1):
        nums_list += locate_numbers(row)
    return sum(nums_list)


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
