from argparse import ArgumentParser
import logging
from pprint import pprint
from itertools import product

from aocd.models import Puzzle


input1 = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

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


def parse_input(input_string: str) -> list[list[str, list[int]]]:
    springs_list = [
        [
            rec1.replace(".", " ") if "," not in rec1 else [int(x) for x in rec1.split(",")]
            for rec1 in one_line.split()
        ]
        for one_line in input_string.splitlines()
    ]
    pprint(springs_list)
    return springs_list


def substitute_values_for_question_marks(spring_row: str, subsitute_values: list[str]) -> str:
    subst_iter = iter(subsitute_values)
    result = "".join([
        next(subst_iter) if one_char == "?" else one_char
        for one_char in spring_row
    ])
    return result


def check_trial(trial_row: str, groups: list[int]) -> int:
    trial_with_spaces = trial_row.replace(".", " ")
    spring_runs = trial_with_spaces.split()
    run_lengths = [
        len(run)
        for run in spring_runs
    ]
    return 1 if run_lengths == groups else 0


def solve_one_spring_row(spring_row: list[str | list[int]]) -> int:
    # can I do a clever regular expression thing?
    # try brute force first
    # print(spring_row[0].count("?"))
    trials = [
        one_trial
        for one_trial in product(" #", repeat=spring_row[0].count("?"))
    ]
    # pprint(trials)
    trials_results = [
        check_trial(
            substitute_values_for_question_marks(spring_row[0], one_trial),
            spring_row[1]
        )
        for one_trial in trials
    ]
    # print(trials_results)
    return sum(trials_results)
    # for one_trial in trials:
    #     trial_str = substitute_values_for_question_marks(spring_row[0], one_trial)
    #     print(trial_str)
    #     test_result = check_trial(trial_str, spring_row[1])
    #     print(test_result)


def _solve(input_string: str) -> int:
    springs_list = parse_input(input_string)
    unknowns_counts = [
        one_spring_row[0].count("?")
        for one_spring_row in springs_list
    ]
    # print(unknowns_counts)
    print(max(unknowns_counts))
    print(len(springs_list))
    # solve_one_spring_row(springs_list[0])
    result = sum([
        solve_one_spring_row(spring_row)
        for spring_row in springs_list
    ])
    return result


def _main():
    puzzle, do_example = _setup()
    if do_example:
        answer = _solve(input1)
        logging.debug(f"example result = {puzzle.examples[0].answer_a}")
    else:
        answer = _solve(puzzle.input_data)
    print(f"answer = {answer}")


if __name__ == "__main__":
    _main()
