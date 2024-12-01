import os
from collections import *
from functools import *
from itertools import *
from math import *

def split_input(inp: list[str]) -> tuple[list[int], list[int]]:
    numbers = [list(map(int, row.split("   "))) for row in inp]
    left = [row[0] for row in numbers]
    right = [row[1] for row in numbers]

    return left, right


def main_part_1(inp: list[str]) -> int:
    left, right = split_input(inp)

    left.sort()
    right.sort()

    ret = 0
    for l, r in zip(left, right):
        ret += abs(l - r)
    
    return ret

def main_part_2(inp: list[str]) -> int:
    left, right = split_input(inp)

    ret = 0
    for i in left:
        ret += i * right.count(i)
    
    return ret

def main() -> None:
    test_input = """3   4
4   3
2   5
1   3
3   9
3   3
"""
    test_input_parsed = test_input.splitlines()
    test_output_part_1_expected = 11
    test_output_part_2_expected = 31

    file_location = os.path.dirname(os.path.realpath(__file__))
    file_location = file_location + "/input.txt"
    with open(file_location, "r") as file:
        input_file = file.readlines()

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
