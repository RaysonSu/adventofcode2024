import os
from collections import *
from functools import *
from itertools import *
from math import *

def get_next(x: int) -> int:
    x ^= x << 6
    x &= 0xffffff
    x ^= x >> 5
    x &= 0xffffff
    x ^= x << 11
    x &= 0xffffff
    return x

def main_part_1(inp: list[str]) -> int:
    total = 0
    for row in inp:
        magic = int(row)
        for _ in range(2000):
            magic = get_next(magic)
        total += magic
    return total

def main_part_2(inp: list[str]) -> int:
    seqs: dict[tuple[int, ...], int] = defaultdict(lambda: 0)

    for row in inp:
        magic = int(row)
        seen: set[tuple[int, ...]] = set()
        buffer: tuple[int, ...] = tuple()

        for _ in range(2000):
            previous_magic = magic
            magic = get_next(magic)
        
            buffer += (magic % 10 - previous_magic % 10,)
            buffer = buffer[-4:]

            if buffer not in seen and len(buffer) == 4:
                seqs[buffer] += magic % 10
                seen.add(buffer)
    
    return max(seqs.values())

def main() -> None:
    test_input = """1
10
100
2024"""
    test_input_parsed = test_input.splitlines()
    test_output_part_1_expected = 37327623
    test_output_part_2_expected = 24

    file_location = os.path.dirname(os.path.realpath(__file__))
    file_location = file_location + "/input.txt"
    with open(file_location, "r") as file:
        input_file = file.read().splitlines()

    test_output_part_1 = main_part_1(test_input_parsed)
    test_output_part_2 = main_part_2(test_input_parsed)

    if test_output_part_1_expected != test_output_part_1:
        print(f"Part 1 testing error: ")
        print(f"Test input: {test_input}")
        print(f"Expected output: {test_output_part_1_expected}")
        print(f"Got: {test_output_part_1}")
        print()

    if test_output_part_2_expected != test_output_part_2:
        print(f"Part 2 testing error: ")
        print(f"Test input: {test_input}")
        print(f"Expected output: {test_output_part_2_expected}")
        print(f"Got: {test_output_part_2}")
        print()

    if test_output_part_1_expected == test_output_part_1:
        print(f"Part 1: {main_part_1(input_file)}")
    
    if test_output_part_2_expected == test_output_part_2:
        print(f"Part 2: {main_part_2(input_file)}")


if __name__ == "__main__":
    main()
