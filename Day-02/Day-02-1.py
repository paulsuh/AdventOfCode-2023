from argparse import ArgumentParser
import logging
from pprint import pprint

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


def parse_game_line(game_line: str) -> tuple[int, list[dict]]:
    game_id_section, _, remainder = game_line.partition(":")

    game_id = int(game_id_section.split()[-1])

    game_plays = [
        {
            one_color.split()[1]: int(one_color.split()[0])
            for one_color in one_play.split(',')
        }
        for one_play in remainder.split("; ")
    ]

    return game_id, game_plays


def check_game(game_plays: list[dict[str, int]]) -> bool:

    blue_count = 0
    green_count = 0
    red_count = 0

    for one_play in game_plays:
        blue_count = max(one_play.get("blue", 0), blue_count)
        green_count = max(one_play.get("green", 0), green_count)
        red_count = max(one_play.get("red", 0), red_count)

    print(blue_count, green_count, red_count)

    return blue_count <= 14 and green_count <= 13 and red_count <= 12


def _solve(input):
    games_total = 0
    for one_game in input.splitlines():

        game_number, plays_list = parse_game_line(one_game)
        if check_game(plays_list):
            games_total += game_number
        else:
            print("xxxx")

    return games_total


def _main():
    puzzle, do_example = _setup()
    if do_example:
        answer = _solve(puzzle.examples[0].input_data)
        logging.debug(f"example result = {puzzle.examples[0].answer_a}")
    else:
        answer = _solve(puzzle.input_data)

    print(answer)


if __name__ == "__main__":
    _main()
