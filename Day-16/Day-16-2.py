import sys
from argparse import ArgumentParser
import logging
from pprint import pprint
from os.path import basename

from aocd.models import Puzzle


input1 = """"""

input2 = """"""

tile_energies: list[list[int]] | None  = None
input_list: list[str] | None = None
ray_passages_list: list[tuple[int, int, int, int]] = []

def _setup() -> tuple[Puzzle, str]:
    parser = ArgumentParser()
    parser.add_argument("-e", "--example", default=None)
    args = parser.parse_args()
    problem_day = int(basename(sys.argv[0]).split("-")[1])
    puzzle = Puzzle(2023, problem_day)
    if args.example is not None:
        logging.getLogger().setLevel("DEBUG")
    return puzzle, args.example


def parse_input(input_string: str) -> None:
    global tile_energies
    global input_list
    input_list = input_string.splitlines()
    tile_energies = [
        [0]*len(input_list[0])
        for row in range(len(input_list))
    ]


def resolve_ray(prev_row: int, prev_col: int,
                 row: int, col: int) -> None:
    global tile_energies
    global input_list
    global ray_passages_list

    while True:
        if row < 0 or col < 0 or row >= len(input_list) or col >= len(input_list[0]):
            # beyond the boundaries
            return

        if (prev_row, prev_col, row, col) in ray_passages_list:
            # already went through this tile in this direction
            return

        # energize this tile
        tile_energies[row][col] = 1

        # record that we went through here
        ray_passages_list.append((prev_row, prev_col, row, col))

        row_delta = row - prev_row
        col_delta = col - prev_col
        prev_row = row
        prev_col = col

        tile_contents = input_list[row][col]
        match tile_contents:
            case ".":
                # continue straight on
                row = row + row_delta
                col = col + col_delta

            case  "/":
                match (row_delta, col_delta):
                    case (1, 0):
                        # enter from above, reflect left
                        col = col - 1
                    case (-1, 0):
                        # enter from below, reflect right
                        col = col + 1
                    case (0, 1):
                        # enter from left, reflect up
                        row = row - 1
                    case (0, -1):
                        # enter from right, reflect down
                        row = row + 1

            case "\\":
                match (row_delta, col_delta):
                    case (1, 0):
                        # enter from above, reflect right
                        col = col + 1
                    case (-1, 0):
                        # enter from below, reflect left
                        col = col - 1
                    case (0, 1):
                        # enter from left, reflect down
                        row = row + 1
                    case (0, -1):
                        # enter from right, reflect up
                        row = row - 1
            case "-":
                match (row_delta, col_delta):
                    case (1, 0) | (-1, 0):
                        # enter from above or below, split left and right
                        resolve_ray(row, col, row, col-1)
                        resolve_ray(row, col, row, col+1)
                        return
                    case (0, 1) | (0, -1):
                        # enter from left or right, continue on
                        col = col + col_delta
            case "|":
                match (row_delta, col_delta):
                    case (0, 1) | (0, -1):
                        # enter from left or right, split up and dowm
                        resolve_ray(row, col, row-1, col)
                        resolve_ray(row, col, row+1, col)
                        return
                    case (1, 0) | (-1, 0):
                        # enter from above or below, continue on
                        row = row + row_delta


def _solve(input_string: str) -> int:
    global tile_energies
    global ray_passages_list

    parse_input(input_string)

    input_width = len(input_list[0])
    input_height = len(input_list)

    result = {}
    # along left edge
    for row in range(input_height):

        # reset records
        tile_energies = [
            [0] * len(input_list[0])
            for row in range(len(input_list))
        ]
        ray_passages_list = []

        resolve_ray(row, -1, row, 0)
        energized_value = sum([
            sum(one_row)
            for one_row in tile_energies
        ])
        print(row, -1, row, 0, energized_value)
        result[(row, -1, row, 0)] = energized_value

    # along right edge
    for row in range(input_height):

        # reset records
        tile_energies = [
            [0] * len(input_list[0])
            for row in range(len(input_list))
        ]
        ray_passages_list = []

        resolve_ray(row, input_width, row, input_width-1)
        energized_value = sum([
            sum(one_row)
            for one_row in tile_energies
        ])
        print(row, input_width, row, input_width-1, energized_value)
        result[(row, input_width, row, input_width-1)] = energized_value

    # along top edge
    for col in range(input_width):

        # reset records
        tile_energies = [
            [0] * len(input_list[0])
            for row in range(len(input_list))
        ]
        ray_passages_list = []

        resolve_ray(-1, col, 0, col)
        energized_value = sum([
            sum(one_row)
            for one_row in tile_energies
        ])
        print(-1, col, 0, col, energized_value)
        result[(-1, col, 0, col)] = energized_value

    # along bottom edge
    for col in range(input_width):

        # reset records
        tile_energies = [
            [0] * len(input_list[0])
            for row in range(len(input_list))
        ]
        ray_passages_list = []

        resolve_ray(input_height, col, input_height-1, col)
        energized_value = sum([
            sum(one_row)
            for one_row in tile_energies
        ])
        print(input_height, col, input_height-1, col, energized_value)
        result[(input_height, col, input_height-1, col)] = energized_value

    # pprint(result)

    return max(result.values())



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
