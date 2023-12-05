from argparse import ArgumentParser
import logging
from pprint import pprint
from sys import argv
from typing import Iterator

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


def create_dict(dict_input: Iterator) -> dict:


    result = KeyDefaultDict()
    while True:

        next_line = next(dict_input)
        if len(next_line) == 0:
            break

        # tuple comprehension
        source_start, dest_start, range_length = (
            int(x)
            for x in next_line.split()
        )
        for source, dest in zip(range(source_start, range_length), range(dest_start, range_length)):
            result[source] = dest

    return result


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

        def __getitem__(self, item):
            if self.source_start <= item < self.source_end:
                return self.dest_start + item - self.source_start
            else:
                return None

    def __init__(self, input_iter: Iterator):
        super().__init__()
        self.range_list = []

        try:
            while True:
                one_line = next(input_iter)
                if len(one_line) == 0:
                    return
                else:
                    self.range_list.append(SparseMapping.MappingRange(one_line))

        except StopIteration:
            pass

    def __getitem__(self, item):
        for one_mapping in self.range_list:
            if (range_result := one_mapping[item]) is not None:
                return range_result
        return item


def parse_input(input_string: str) -> tuple[list[int], list[SparseMapping]]:

    input_iter = iter(input_string.splitlines())

    seed_line = next(input_iter)
    seeds_list = [
        int(x)
        for x in seed_line.split(":")[1].split()
    ]
    _ = next(input_iter)    # discard blank line

    mappings_list = []
    try:
        while True:
            line = next(input_iter)     # mapping name
            mappings_list.append(SparseMapping(input_iter))

    except StopIteration:
        pass

    return seeds_list, mappings_list


def process_seed(seed_num: int, mappings_list: list[SparseMapping]) -> int:

    result = seed_num
    for one_mapping in mappings_list:
        result = one_mapping[result]

    return result


def _solve(input: str) -> int:

    seeds_list, mappings_list = parse_input(input)

    min_location = max(seeds_list)
    min_seed = -1

    for one_seed in seeds_list:
        location = process_seed(one_seed, mappings_list)
        if location < min_location:
            min_location = location
            min_seed = one_seed

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
