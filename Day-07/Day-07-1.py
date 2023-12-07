from argparse import ArgumentParser
import logging
from pprint import pprint
from enum import IntEnum

from aocd.models import Puzzle


class HandType(IntEnum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6

trick_translator = str.maketrans("TJQKA", "ABCDE")


def _setup() -> tuple[Puzzle, str]:
    parser = ArgumentParser()
    parser.add_argument("-e", "--example", default=None)
    parser.add_argument("day_number", type=int)
    args = parser.parse_args()
    puzzle = Puzzle(2023, args.day_number)
    if args.example is not None:
        logging.getLogger().setLevel("DEBUG")
    return puzzle, args.example


def parse_input(input_string: str) -> list[tuple[str, int]]:
    input_lines = input_string.splitlines()

    result = []
    for one_line in input_lines:
        hand, bid = one_line.split()
        # Python trick - 23456789TJQKA
        # becomes      - 23456789ABCDE
        # this lets Python's natural sort algorithm just work
        result.append(
            (determine_hand_type(hand), hand.translate(trick_translator),
             hand, int(bid))
        )
    return result


def determine_hand_type(hand: str) -> HandType:

    unique_chars = list(set(hand))
    num_unique_chars = len(unique_chars)
    if num_unique_chars == 1:
        return HandType.FIVE_OF_A_KIND
    elif num_unique_chars == 5:
        return HandType.HIGH_CARD
    elif num_unique_chars == 4:
        return HandType.ONE_PAIR
    elif num_unique_chars == 2:
        # could be Four of a kind or Full house
        if hand.count(unique_chars[0]) == 4 or hand.count(unique_chars[1]) == 4:
            return HandType.FOUR_OF_A_KIND
        else:
            return HandType.FULL_HOUSE

    # num_unique_chars == 3 could be Three of a kind or Two pair
    elif hand.count(unique_chars[0]) == 3 or hand.count(unique_chars[1]) == 3 or hand.count(unique_chars[2]) == 3:
        return HandType.THREE_OF_A_KIND
    else:
        return HandType.TWO_PAIR


def _solve(input_string: str) -> int:
    hands_list = parse_input(input_string)

    hands_list.sort()
    # print(hands_list)
    value_list = [
        hand[3] * rank
        for hand, rank in zip(hands_list, range(1, len(hands_list)+1))
    ]
    return sum(value_list)


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
