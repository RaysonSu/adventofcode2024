import os
from collections import *
from functools import *
from itertools import *
from math import *
import re


def main_part_1(inp: list[str]) -> int:
    total = 0

    for left, right in re.findall(r"mul\((\d+),(\d+)\)", "\n".join(inp)):
        total += int(left) * int(right)
    
    return total

def main_part_2(inp: list[str]) -> int:
    total = 0
    
    active = True
    for group in re.findall(r"(mul\(\d+,\d+\)|do\(\)|don't\(\))", "\n".join(inp)):
        if group == "do()":
            active = True
        elif group == "don't()":
            active = False
        elif active:
            left, right = re.findall(r"(\d+),(\d+)", group)[0]
            total += int(left) * int(right)
        
    return total

def main() -> None:
    test_input = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""
    test_input_parsed = test_input.splitlines()
    test_output_part_1_expected = 161
    test_output_part_2_expected = 48

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
