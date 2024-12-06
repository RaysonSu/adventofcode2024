import os
from collections import *
from functools import *
from itertools import *
from math import *


def main_part_1(inp: list[str]) -> int:
    page_start_index = inp.index("")
    rules = [tuple(rule.split("|")) for rule in inp[:page_start_index]]
    pages = [page.split(",") for page in inp[page_start_index + 1:]]

    total = 0
    for page in pages:
        for left, right in rules:
            if left in page and right in page \
            and page.index(left) > page.index(right):
                break
        else:
            total += int(page[len(page) // 2])

    return total

def main_part_2(inp: list[str]) -> int:
    page_start_index = inp.index("")
    rules = [tuple(rule.split("|")) for rule in inp[:page_start_index]]
    pages = [page.split(",") for page in inp[page_start_index + 1:]]

    def cmp(left: str, right: str) -> int:
        if (left, right) in rules:
            return 1
        elif (right, left) in rules:
            return -1
        else:
            return 0


    total = 0
    for page in pages:
        for left, right in rules:
            if left in page and right in page \
            and page.index(left) > page.index(right):
                
                page.sort(key=cmp_to_key(cmp))
                total += int(page[len(page) // 2])
                break

    return total

def main() -> None:
    test_input = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""
    test_input_parsed = test_input.splitlines()
    test_output_part_1_expected = 143
    test_output_part_2_expected = 123

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
