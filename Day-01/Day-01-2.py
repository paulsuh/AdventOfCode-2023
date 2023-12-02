from argparse import ArgumentParser
import logging
from typing import Optional

from aocd.models import Puzzle


numbers = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine"
]

def _setup() -> tuple[Puzzle, str]:
    parser = ArgumentParser()
    parser.add_argument("-e", "--example", default=None)
    parser.add_argument("day_number", type=int)
    args = parser.parse_args()
    puzzle = Puzzle(2023, args.day_number)
    if args.example is not None:
        logging.getLogger().setLevel("DEBUG")
    return puzzle, args.example


def _get_actual_digit(line: str, position: int) -> str:
    if line[position].isdigit():
        return line[position]
    for word in numbers:
        if line[position:].startswith(word):
            return str(numbers.index(word))
    raise RuntimeError(f"line = {line}, position={position}")


def _scan_line(line:str) -> list[str]:

    digit_positions = []

    # find leftmost and rightmost digits
    for digit in "123456789":
        digit_positions.append(
            line.find(digit)
        )
        digit_positions.append(
            line.rfind(digit)
        )

    # find leftmost and rightmost spelled out words
    for word in numbers:
        digit_positions.append(
            line.find(word)
        )
        digit_positions.append(
            line.rfind(word)
        )

    left_pos = min([
        x
        for x in digit_positions
        if x != -1
    ])
    right_pos = max(digit_positions)

    return [
        _get_actual_digit(line, left_pos),
        _get_actual_digit(line, right_pos)
    ]


def _solve(input: str):
    result = 0
    for one_line in input.splitlines():
        line_digits = _scan_line(one_line)
        logging.debug(line_digits)
        result += int(line_digits[0]+line_digits[-1])

    return result


def _main():
    puzzle, do_example = _setup()
    if do_example:
        answer = _solve("""two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen""")
        logging.debug(f"example result = {puzzle.examples[0].answer_b}")
    else:
        answer = _solve(puzzle.input_data)

    print(answer)


if __name__ == "__main__":
    _main()
