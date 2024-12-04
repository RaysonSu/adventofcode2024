import os
from collections import *
from functools import *
from itertools import *
from math import *


def main_part_1(inp: list[str]) -> int:
    total = 0

    for y, x in product(range(len(inp)), range(len(inp[0]))):
        if inp[y][x] != "X":
            continue

        for dx, dy in product([-1, 0, 1], [-1, 0, 1]):
            if  0 <= y + 3 * dy < len(inp) \
            and 0 <= x + 3 * dx < len(inp[0]) \
            and inp[y + dy][x + dx] \
                + inp[y + 2 * dy][x + 2 * dx] \
                + inp[y + 3 * dy][x + 3 * dx] == "MAS":

                total += 1

    return total

def main_part_2(inp: list[str]) -> int:
    total = 0

    for y, x in product(range(len(inp)), range(len(inp[0]))):
        if inp[y][x] == "A" \
        and 0 < x < len(inp[0]) - 1 \
        and 0 < y < len(inp) - 1 \
        and inp[y + 1][x + 1] + inp[y - 1][x - 1] in "MSM" \
        and inp[y + 1][x - 1] + inp[y - 1][x + 1] in "MSM":
            
            total += 1

    return total

def main() -> None:
    test_input = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""
    test_input_parsed = test_input.splitlines()
    test_output_part_1_expected = 18
    test_output_part_2_expected = 9

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
