import os
from collections import *
from functools import *
from itertools import *
from math import *

def is_safe(array: list[int]) -> bool:
    if len(array) < 2:
        return True
    
    if array[0] == array[1]:
        return False
    
    sign = array[1] - array[0]
    sign //= abs(sign)

    for left, right in zip(array, array[1:]):
        delta = (right - left) * sign
        if not (1 <= delta <= 3):
            return False
    
    return True

def main_part_1(inp: list[str]) -> int:
    ret = 0

    for row in inp:
        ret += is_safe(list(map(int, row.split(" "))))
    
    return ret

def main_part_2(inp: list[str]) -> int:
    ret = 0
    
    for row in inp:
        data = list(map(int, row.split(" ")))

        safe = is_safe(data)
        for i in range(len(data)):
            tmp = data.copy()
            tmp.pop(i)
            if is_safe(tmp):
                safe = True
                break
        
        if safe:
            ret += 1
    
    return ret

def main() -> None:
    test_input = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""
    test_input_parsed = test_input.splitlines()
    test_output_part_1_expected = 2
    test_output_part_2_expected = 4

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
