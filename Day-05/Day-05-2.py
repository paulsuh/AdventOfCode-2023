from argparse import ArgumentParser
import logging
from pprint import pprint
from sys import argv
from typing import Iterator, Optional
from more_itertools import grouper
from functools import cache
from datetime import datetime

from aocd.models import Puzzle


mappings_list = []


def _setup() -> tuple[Puzzle, str]:
    parser = ArgumentParser()
    parser.add_argument("-e", "--example", default=None)
    parser.add_argument("day_number", type=int)
    args = parser.parse_args()
    puzzle = Puzzle(2023, args.day_number)
    if args.example is not None:
        logging.getLogger().setLevel("DEBUG")
    return puzzle, args.example


class SparseMapping(dict):

    class MappingRange(dict):

        def __init__(self, mapping_line: str):
            super().__init__()
            dest_start, source_start, range_len = (
                int(x)
                for x in mapping_line.split()
            )
            self.source_start = source_start
            self.dest_start = dest_start
            self.source_end = source_start + range_len

        def __getitem__(self, item: int) -> Optional[int]:
            if self.source_start <= item < self.source_end:
                return self.dest_start + item - self.source_start
            else:
                return None

    def __init__(self, name: str, input_iter: Iterator):
        super().__init__()
        self.range_list = []
        self.name = name
        self._hash_value = hash(name)

        try:

            while True:
                one_line = next(input_iter)
                if len(one_line) == 0:
                    return
                else:
                    self.range_list.append(SparseMapping.MappingRange(one_line))

        except StopIteration:
            pass

    # @cache
    def __getitem__(self, item: int) -> int:
        for one_mapping in self.range_list:
            if (range_result := one_mapping[item]) is not None:
                return range_result
        return item

    def __hash__(self):
        return self._hash_value

    def __eq__(self, other):
        return self._hash_value == other._hash_value


def parse_input(input_string: str) -> list[int]:

    global mappings_list

    input_iter = iter(input_string.splitlines())

    seed_line = next(input_iter)
    seeds_list = [
        int(x)
        for x in seed_line.split(":")[1].split()
    ]
    print(f"seeds to be run = {sum(seeds_list[1::2])}")
    _ = next(input_iter)    # discard blank line

    mappings_list = []
    try:
        while True:
            name = next(input_iter)
            mappings_list.append(SparseMapping(name, input_iter))

    except StopIteration:
        pass

    return seeds_list


def process_seed(seed_num: int) -> int:

    global mappings_list

    result = seed_num
    for one_mapping in mappings_list:
        result = one_mapping[result]

    return result


def _solve(input_string: str) -> int:

    seeds_list = parse_input(input_string)

    min_location = max(seeds_list)
    min_seed = -1

    seed_pairs_run_so_far = 0
    seed_pairs_total = len(seeds_list) // 2
    for seed_start, seed_run in grouper(seeds_list, 2):

        seed_pairs_run_so_far += 1
        print(f"running seed pair {seed_pairs_run_so_far} of {seed_pairs_total}")
        print(f"seed types to be checked = {seed_run}")
        start = datetime.now()
        seeds_run_so_far = 0

        for one_seed in range(seed_start, seed_start+seed_run):

            seeds_run_so_far += 1
            if seeds_run_so_far % 1000000 == 0:
                print(f"seeds run so far = {seeds_run_so_far}")

            location = process_seed(one_seed)
            if location < min_location:
                min_location = location
                min_seed = one_seed

        end = datetime.now()
        print(f"{seed_run} pairs checked in {end - start}")

    return min_location


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
