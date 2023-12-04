from argparse import ArgumentParser
import logging
from pprint import pprint
from sys import argv

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


def convert_to_int_list(numbers_string: str) -> list[int]:
    result = [
        int(x)
        for x in numbers_string.split()
    ]
    return result


def parse_card(card_line: str) -> tuple[list[int], list[int]]:

    _, card_nums = card_line.split(":")
    winning_nums_string, my_nums_string = card_nums.split("|")
    winning_nums_list = convert_to_int_list(winning_nums_string)
    my_nums_list = convert_to_int_list(my_nums_string)
    return winning_nums_list, my_nums_list


def card_value(card_line: str) -> int:
    winning_numbers, my_numbers = parse_card(card_line)
    winning_set = set(winning_numbers)
    my_set = set(my_numbers)
    number_of_matches = len(winning_set & my_set)
    if number_of_matches > 0:
        return 2 ** (number_of_matches -1)
    else:
        return 0


def _solve(input: str) -> int:
    result = 0
    for one_card in input.splitlines():
        result += card_value(one_card)
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
