import os
from collections import *
from functools import *
from itertools import *
from math import *
from typing import Any

def is_valid_location(x: int, y: int, 
                      antenna_locations: dict[Any, list[tuple[int, int]]]) -> bool:

    for locations in antenna_locations.values():
        for p1, p2 in permutations(locations, 2):
            if (p2[1] - p1[1]) * (x - p1[0]) \
            == (y - p1[1]) * (p2[0] - p1[0]) : # modified version of the gradient formula
                return True
    
    return False

def main_part_1(inp: list[str]) -> int:
    antenna_locations: dict[str, list[tuple[int, int]]] = defaultdict(lambda:[])
    
    for y, row in enumerate(inp):
        for x, char in enumerate(row):
            if char != ".":
                antenna_locations[char].append((x, y))
    
    antinodes: set[tuple[int, int]] = set()
    for locations in antenna_locations.values():
        for p1, p2 in permutations(locations, 2):
            x0 = 2 * p2[0] - p1[0]
            y0 = 2 * p2[1] - p1[1]
        
            if 0 <= x0 < len(inp[0]) \
            and 0 <= y0 < len(inp):
                antinodes.add((x0, y0))

    return len(antinodes)

def main_part_2(inp: list[str]) -> int:
    antenna_locations: dict[str, list[tuple[int, int]]] = defaultdict(lambda:[])
    
    for y, row in enumerate(inp):
        for x, char in enumerate(row):
            if char != ".":
                antenna_locations[char].append((x, y))

    antinodes = 0
    for x, y in product(range(len(inp[0])), range(len(inp))):
        if is_valid_location(x, y, antenna_locations):
            antinodes += 1

    return antinodes

def main() -> None:
    test_input = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""
    test_input_parsed = test_input.splitlines()
    test_output_part_1_expected = 14
    test_output_part_2_expected = 34

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
