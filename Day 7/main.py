import os
from collections import *
from functools import *
from itertools import *
from math import *

def is_possible(target: int, values: list[int], allow_concat: bool = False) -> bool:
    if len(values) == 1:
        return target == values[0]

    if target < values[-1]:
        return False
    
    current = values[-1]
    remaining = values[:-1]

    return is_possible(target - current, remaining, allow_concat) \
    or (target % current == 0 and is_possible(target // current, remaining, allow_concat)) \
    or (allow_concat and str(target).endswith(str(current)) and target != current \
        and is_possible(int(str(target)[:-len(str(current))]), remaining, allow_concat))

def main_part_1(inp: list[str]) -> int:
    total = 0

    for row in inp:
        target = int(row.split(": ")[0])
        values = list(map(int, row.split(": ")[1].split(" ")))
            
        if is_possible(target, values):
            total += target
    
    return total

def main_part_2(inp: list[str]) -> int:
    total = 0

    for row in inp:
        target = int(row.split(": ")[0])
        values = list(map(int, row.split(": ")[1].split(" ")))
            
        if is_possible(target, values, True):
            total += target
    
    return total

def main() -> None:
    test_input = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""
    test_input_parsed = test_input.splitlines()
    test_output_part_1_expected = 3749
    test_output_part_2_expected = 11387

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
