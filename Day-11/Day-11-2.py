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


def expand_galaxy_locations(galaxies_list: list[list[int, int]],
                            rows_to_expand: list[int],
                            cols_to_expand: list[int]) -> list[list[int, int]]:

    for one_galaxy in galaxies_list:

        row_expansion_factor = 0
        for one_row in rows_to_expand:
            if one_galaxy[0] > one_row:
                row_expansion_factor += 1
        one_galaxy[0] = (1000000-1) * row_expansion_factor + one_galaxy[0]

        col_expansion_factor = 0
        for one_col in cols_to_expand:
            if one_galaxy[1] > one_col:
                col_expansion_factor += 1
        one_galaxy[1] = (1000000-1) * col_expansion_factor + one_galaxy[1]

    return galaxies_list


def locate_galaxies(galaxy_map: list[str]) -> list[list[int, int]]:
    result = []
    for row, row_num in zip(galaxy_map, range(len(galaxy_map))):
        for col_char, col_num in zip(row, range(len(row))):
            if col_char == "#":
                result.append([row_num, col_num])

    return result


def _solve(input_string: str) -> int:
    galaxy_map = parse_input(input_string)
    galaxies_list = locate_galaxies(galaxy_map)

    print(galaxies_list)

    empty_cols = locate_empty_columns(galaxy_map)
    empty_rows = locate_empty_rows(galaxy_map)

    galaxies_list = expand_galaxy_locations(
        galaxies_list, empty_rows, empty_cols
    )

    print(galaxies_list)

    print(len(list(combinations(galaxies_list, 2))))
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
