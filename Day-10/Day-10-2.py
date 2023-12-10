from argparse import ArgumentParser
import logging
from pprint import pprint
from itertools import product

from aocd.models import Puzzle
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely import contains_xy


input1 = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF
"""

input2 = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
"""

input3 = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""

input4 = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""

input5 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""

# up, right, down, left
connections_dict = {
    "|": ((-1, 0), (1, 0)),
    "-": ((0, -1), (0, 1)),
    "L": ((-1, 0), (0, 1)),
    "J": ((-1, 0), (0, -1)),
    "7": ((0, -1), (1, 0)),
    "F": ((0, 1), (1, 0)),
    ".": ()
}


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
    # put a row of dots before and after
    # put a dot before and after each row
    # this lets us test adjacency without doing bounds checks
    result = [
        f".{one_line}."
        for one_line in input_string.splitlines()
    ]
    result.insert(0, "."*len(result[0]))
    result.append("."*len(result[0]))

    return result


def find_start(pipes_list: list[str]) -> tuple[int, int]:
    for one_line, row_num in zip(pipes_list, range(len(pipes_list))):
        if (col_num := one_line.find("S")) >= 0:
            return row_num, col_num


def find_next_pipes_start(pipes_list: list[str], start_loc: tuple[int, int]) -> tuple[tuple[int, int]]:

    # search up, down, left, right for connecting pipes
    connections = []
    # up
    if (pipes_list[start_loc[0]-1][start_loc[1]] == "|") or \
        (pipes_list[start_loc[0]-1][start_loc[1]] == "7") or \
        (pipes_list[start_loc[0]-1][start_loc[1]] == "F"):
        connections.append((start_loc[0]-1, start_loc[1]))
    # down
    if (pipes_list[start_loc[0]+1][start_loc[1]] == "|") or \
        (pipes_list[start_loc[0]+1][start_loc[1]] == "L") or \
        (pipes_list[start_loc[0]+1][start_loc[1]] == "J"):
        connections.append((start_loc[0]+1, start_loc[1]))
    # left
    if (pipes_list[start_loc[0]][start_loc[1]-1] == "-") or \
        (pipes_list[start_loc[0]][start_loc[1]-1] == "L") or \
        (pipes_list[start_loc[0]][start_loc[1]-1] == "F"):
        connections.append((start_loc[0], start_loc[1]-1))
    # down
    if (pipes_list[start_loc[0]][start_loc[1]+1] == "-") or \
        (pipes_list[start_loc[0]][start_loc[1]+1] == "J") or \
        (pipes_list[start_loc[0]][start_loc[1]+1] == "7"):
        connections.append((start_loc[0], start_loc[1]+1))

    result = tuple(connections)
    connections_dict["S"] = result

    return result


def find_next_pipe(pipes_list: list[str],
                   prev_pipe: tuple[int, int],
                   current_pipe: tuple[int, int]) -> tuple[int, int]:

    for one_connection in connections_dict[pipes_list[current_pipe[0]][current_pipe[1]]]:

        possible_next_pipe = (current_pipe[0]+one_connection[0],
                              current_pipe[1] + one_connection[1])
        if possible_next_pipe != prev_pipe:
            return possible_next_pipe


def check_for_points_inside(pipes_list: list[str],
                            points_list_a: list[tuple[int, int]],
                            points_list_b: list[tuple[int, int]]) -> int:
    combined_path_list = points_list_a + list(reversed(points_list_b))
    # print(combined_path_list)

    path_polygon = Polygon(combined_path_list)
    # print(path_polygon)

    result = 0
    for one_coord in product(range(len(pipes_list)), range(len(pipes_list[0]))):
        # point = Point(one_coord)
        # print(point)
        if contains_xy(path_polygon, *one_coord):
            print(one_coord)
            result += 1

    return result


def _solve(input_string: str) -> int:
    pipes_list = parse_input(input_string)
    # pprint(pipes_list, width=7)
    start_cell = find_start(pipes_list)
    print(f"start = {start_cell}")
    next_cells = find_next_pipes_start(pipes_list, start_cell)
    print(next_cells)
    branch_a = [start_cell, next_cells[0]]
    branch_b = [start_cell, next_cells[1]]
    while branch_a[-1] != branch_b[-1]:
        branch_a.append(find_next_pipe(pipes_list,
                                      branch_a[-2],
                                      branch_a[-1]))
        branch_b.append(find_next_pipe(pipes_list,
                                      branch_b[-2],
                                      branch_b[-1]))

    # pprint(branch_a)
    # pprint(branch_b)

    result = check_for_points_inside(pipes_list, branch_a, branch_b)
    return result


def _main():
    puzzle, do_example = _setup()
    if do_example:
        answer = _solve(input5)
        logging.debug(f"example result = {puzzle.examples[0].answer_a}")
    else:
        answer = _solve(puzzle.input_data)
    print(f"answer = {answer}")


if __name__ == "__main__":
    _main()
