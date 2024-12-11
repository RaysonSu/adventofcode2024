import os
from collections import *
from functools import *
from itertools import *
from math import *


@lru_cache(maxsize=1048576)
def simulate_blinks(stone: int, iterations: int) -> int:
    if iterations <= 0:
        return 1
    
    if stone == 0:
        return simulate_blinks(1, iterations - 1)

    if len(str(stone)) % 2 == 0:
        return simulate_blinks(int(str(stone)[:len(str(stone)) // 2]), iterations - 1) \
            + simulate_blinks(int(str(stone)[len(str(stone)) // 2:]), iterations - 1)

    return simulate_blinks(stone * 2024, iterations - 1)

def main_part_1(inp: list[str]) -> int:
    total = 0
    for stone in list(map(int, inp[0].split(" "))):
        total += simulate_blinks(stone, 25)
    
    return total

def main_part_2(inp: list[str]) -> int:
    total = 0
    for stone in list(map(int, inp[0].split(" "))):
        total += simulate_blinks(stone, 75)
    
    return total

def main() -> None:
    test_input = """125 17"""
    test_input_parsed = test_input.splitlines()
    test_output_part_1_expected = 55312

    file_location = os.path.dirname(os.path.realpath(__file__))
    file_location = file_location + "/input.txt"
    with open(file_location, "r") as file:
        input_file = file.read().splitlines()

    test_output_part_1 = main_part_1(test_input_parsed)

    if test_output_part_1_expected != test_output_part_1:
        print(f"Part 1 testing error: ")
        print(f"Test input: {test_input}")
        print(f"Expected output: {test_output_part_1_expected}")
        print(f"Got: {test_output_part_1}")
        print()

    if test_output_part_1_expected == test_output_part_1:
        print(f"Part 1: {main_part_1(input_file)}")
        print(f"Part 2: {main_part_2(input_file)}")


if __name__ == "__main__":
    main()
