from argparse import ArgumentParser
import logging
from pprint import pprint
from itertools import combinations

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
    galaxy_map = input_string.splitlines()
    return galaxy_map


def locate_empty_rows(galaxy_map: list[str]) -> list[int]:

    result = [
        row_num
        for row_content, row_num in zip(galaxy_map, range(len(galaxy_map)))
        if "#" not in row_content
    ]
    return result


def locate_empty_columns(galaxy_map: list[str]) -> list[int]:

    cols = zip(*galaxy_map, strict=True)
    result = [
        col_num
        for column_content, col_num in zip(cols, range(len(galaxy_map[0])))
        if "#" not in column_content
    ]
    return result


def expand_cols_in_one_row(row:str, cols_to_expand: list[int]) -> str:

    new_row = list(row)
    for one_col in reversed(cols_to_expand):
        new_row[one_col:one_col] = ["."]

    return "".join(new_row)


def expand_cols(galaxy_map: list[str], cols_to_expand: list[int]) -> list[str]:
    new_map = []
    for one_row in galaxy_map:
        new_map.append(expand_cols_in_one_row(one_row, cols_to_expand))
    return new_map


def expand_rows(galaxy_map: list[str]) -> list[str]:

    new_map = []
    for one_row in galaxy_map:
        if "#" not in one_row:
            new_map.append(one_row)
        new_map.append(one_row)

    return new_map


def locate_galaxies(galaxy_map: list[str]) -> list[tuple[int, int]]:
    result = []
    for row, row_num in zip(galaxy_map, range(len(galaxy_map))):
        for col_char, col_num in zip(row, range(len(row))):
            if col_char == "#":
                result.append((row_num, col_num))

    return result


def _solve(input_string: str) -> int:
    galaxy_map = parse_input(input_string)

    empty_cols = locate_empty_columns(galaxy_map)
    galaxy_map = expand_cols(galaxy_map, empty_cols)
    galaxy_map = expand_rows(galaxy_map)

    galaxies_list = locate_galaxies(galaxy_map)
    distances = [
        abs(one_pair[0][0]-one_pair[1][0]) + abs(one_pair[0][1]-one_pair[1][1])
        for one_pair in combinations(galaxies_list, 2)
    ]
    return sum(distances)


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
