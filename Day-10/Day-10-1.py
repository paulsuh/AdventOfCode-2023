from argparse import ArgumentParser
import logging
from pprint import pprint

from aocd.models import Puzzle


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


def find_next_pipes_start(pipes_list: list[str], start_loc: tuple[int, int]) -> list[tuple[int, int]]:

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


def _solve(input_string: str) -> int:
    pipes_list = parse_input(input_string)
    pprint(pipes_list, width=7)
    start_cell = find_start(pipes_list)
    print(f"start = {start_cell}")
    next_cells = find_next_pipes_start(pipes_list, start_cell)
    print(next_cells)
    branchA = [start_cell, next_cells[0]]
    branchB = [start_cell, next_cells[1]]
    while branchA[-1] != branchB[-1]:
        branchA.append(find_next_pipe(pipes_list,
                                      branchA[-2],
                                      branchA[-1]))
        branchB.append(find_next_pipe(pipes_list,
                                      branchB[-2],
                                      branchB[-1]))

    pprint(branchA)
    pprint(branchB)
    return len(branchA) - 1


def _main():
    puzzle, do_example = _setup()
    if do_example:
        answer = _solve(input2)
        logging.debug(f"example result = {puzzle.examples[0].answer_a}")
    else:
        answer = _solve(puzzle.input_data)
    print(f"answer = {answer}")


if __name__ == "__main__":
    _main()
