import sys
from argparse import ArgumentParser
import logging
from pprint import pprint
from os.path import basename
from sys import setrecursionlimit
from shapely.geometry.polygon import Polygon
from shapely import contains_xy, area

from aocd.models import Puzzle

input1 = """"""

input2 = """"""


def _setup() -> tuple[Puzzle, str]:
    parser = ArgumentParser()
    parser.add_argument("-e", "--example", default=None)
    args = parser.parse_args()
    problem_day = int(basename(sys.argv[0]).split("-")[1])
    puzzle = Puzzle(2023, problem_day)
    if args.example is not None:
        logging.getLogger().setLevel("DEBUG")
    return puzzle, args.example


def parse_input(input_string: str) -> list[list[str]]:
    input_list = input_string.splitlines()
    result = [
        one_line.split()
        for one_line in input_list
    ]

    return result


def plot_boundary(input_list: list[list[str]]) -> tuple[list[tuple[int, int]], int]:

    # start at 0,0
    # record every block
    blocks_list = [(0, 0)]
    current_row = 0
    current_col = 0
    trench_len = 0
    for one_trench in input_list:
        # print(one_trench)
        trench_len += int(one_trench[1])
        match one_trench[0]:
            case 'U':
                # pprint(addition)
                # additions = [
                #     (current_row-i, current_col)
                #     for i in range(1, int(one_trench[1])+1)
                # ]
                # blocks_list += additions
                current_row = current_row - int(one_trench[1])
                next_block = (current_row, current_col)
                blocks_list.append(next_block)
                # print(current_row)
            case 'D':
                # additions = [
                #     (current_row+i, current_col)
                #     for i in range(1, int(one_trench[1])+1)
                # ]
                # blocks_list += additions
                current_row = current_row + int(one_trench[1])
                next_block = (current_row, current_col)
                blocks_list.append(next_block)
                # print(current_row)
            case 'R':
                # additions = [
                #     (current_row, current_col+i)
                #     for i in range(1, int(one_trench[1])+1)
                # ]
                # blocks_list += additions
                current_col = current_col + int(one_trench[1])
                next_block = (current_row, current_col)
                blocks_list.append(next_block)
                # print(current_row)
            case 'L':
                # additions = [
                #     (current_row, current_col-i)
                #     for i in range(1, int(one_trench[1])+1)
                # ]
                # blocks_list += additions
                current_col = current_col - int(one_trench[1])
                next_block = (current_row, current_col)
                blocks_list.append(next_block)
                # print(current_row)

    return blocks_list, trench_len


def dig_out_center(trench: list[tuple[int, int]]) -> int:

    row_values = [x[0] for x in trench]
    col_values = [x[1] for x in trench]
    min_row = min(row_values)
    max_row = max(row_values)
    min_col = min(col_values)
    max_col = max(col_values)
    print(min_row, max_row, min_col, max_col)

    path_polygon = Polygon(trench)

    print(path_polygon)

    result = 0
    for row in range(min_row, max_row):
        for col in range(min_col, max_col):
            if contains_xy(path_polygon, row, col):
                result += 1

    return result


def _solve(input_string: str) -> int:

    input_list = parse_input(input_string)
    # pprint(input_list)
    trench, trench_len = plot_boundary(input_list)
    # pprint(trench)
    print(trench_len)

    inside_count = dig_out_center(trench)
    print(inside_count)

    return trench_len+inside_count
    # print((max_row-min_row+3)*(max_col-min_col+3))
    # exterior_blocks = dig_out_center(trench)
    # # pprint(exterior_blocks)
    # print(len(exterior_blocks))
    # result = (max_row-min_row+3)*(max_col-min_col+3) - len(exterior_blocks)
    # return result


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
