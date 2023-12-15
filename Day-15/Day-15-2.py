import sys
from argparse import ArgumentParser
import logging
from pprint import pprint
from os.path import basename
from functools import reduce
from collections import defaultdict

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


def parse_input(input_string: str) -> list[str]:
    # print(input_string)
    input_list = input_string.split(",")
    return input_list


def aoc_hash(input_step: str) -> int:
    return reduce(
        lambda acc, next_char: ((acc+ord(next_char))*17) % 256,
        input_step,
        0
    )


def _solve(input_string: str) -> int:
    input_list = parse_input(input_string)
    lens_boxes = defaultdict(dict)
    for one_step in input_list:
        if one_step[-2] == "=":
            label = one_step[0:-2]
            box_num = aoc_hash(label)
            lens_power = one_step[-1]
            box = lens_boxes[box_num]
            box[label] = lens_power
        else:
            label = one_step[0:-1]
            box_num = aoc_hash(label)
            box = lens_boxes[box_num]
            if label in box:
                del box[label]

    print(lens_boxes)
    lens_list = [
        (box_num + 1) * slot_num * int(one_lens)
        for box_num, lenses_in_box in lens_boxes.items()
        for slot_num, one_lens in enumerate(lenses_in_box.values(), 1)
    ]
    print(lens_list)
    return sum(lens_list)


def _main():
    puzzle, do_example = _setup()
    if do_example:
        answer = _solve(puzzle.examples[0].input_data)
        logging.debug(f"example result = {puzzle.examples[0].answer_b}")
    else:
        answer = _solve(puzzle.input_data)
    print(f"answer = {answer}")


if __name__ == "__main__":
    _main()
