import os
from collections import *
from typing import *
from functools import *
from itertools import *
from math import *

def checker(towels: list[str]) -> Callable[[str], bool]:
    @cache
    def valid(design: str) -> bool:
        if not design:
            return True
        
        for towel in towels:
            if design.startswith(towel) \
            and valid(design[len(towel):]):
                return True
        
        return False
    
    return valid

def counter(towels: list[str]) -> Callable[[str], int]:
    @cache
    def count(towel: str) -> int:
        if not towel:
            return 1
        
        possibilities = 0
        for t in towels:
            if towel.startswith(t):
                possibilities += count(towel[len(t):])
        
        return possibilities
    
    return count

def main_part_1(inp: list[str]) -> int:
    check = checker(inp[0].split(", "))

    total = 0
    for design in inp[2:]:
        if check(design):
            total += 1
    
    return total

def main_part_2(inp: list[str]) -> int:
    count = counter(inp[0].split(", "))

    total = 0
    for design in inp[2:]:
        total += count(design)
    
    return total


def main() -> None:
    test_input = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""
    test_input_parsed = test_input.splitlines()
    test_output_part_1_expected = 6
    test_output_part_2_expected = 16

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
