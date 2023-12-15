from argparse import ArgumentParser
import logging
from pprint import pprint
from typing import Iterator

from aocd.models import Puzzle


input1 = """"""

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


def parse_input(input_string: str) -> list[str]:
    # print(input_string)
    return input_string.splitlines()


def rotate_board_90_right(board: list[str]) -> list[list[str]]:
    # with Python it's easiest to work with a
    # single row rather than across rows
    # result = list(list(zip(*board[::-1])))
    # result2 = [
    #     list(row)
    #     for row in result
    # ]
    result = [
        list(x)
        for x in zip(*board[::-1])
    ]
    return result


def rotate_board_90_left(board: list[str]) -> list[list[str]]:
    result = [
        list(x)
        for x in zip(*board)
    ][::-1]
    return result

def roll_rocks_left(board: list[list[str]]):
    for one_row in board:
        prev_stop = 0
        for index in range(len(one_row)):
            # start at that location, search leftwards for
            # something not "."
            if one_row[index] == "#":
                prev_stop = index+1
            elif one_row[index] == ".":
                pass
            elif index == prev_stop:   # == "O" and doesn't have room to roll
                prev_stop = index + 1
            else:                       # == "O" and can roll
                one_row[prev_stop] = "O"
                one_row[index] = "."
                prev_stop = prev_stop+1


def calculate_weight(board: list[list[str]]) -> int:
    # transform row to 1's and 0's
    # dot product with [10 9 8 ...]
    result = 0
    for one_row in board:
        # print(one_row)
        row_counts = [
            1 if item == "O" else 0
            for item in one_row
        ]
        # print(row_counts)

        row_value = sum([
            value * item
            for value, item in zip(range(len(one_row), 0, -1), row_counts)
        ])
        # print(row_value)
        result += row_value

    return result


def _solve(input_string: str) -> int:
    input_list = parse_input(input_string)
    rotated_board = rotate_board_90_left(input_list)
    pprint(input_list)
    pprint(rotated_board)
    roll_rocks_left(rotated_board)
    pprint(rotated_board)
    result = calculate_weight(rotated_board)
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
