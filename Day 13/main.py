import os
from collections import *
from functools import *
from itertools import *

def main_part_1(inp: list[str]) -> int:
    total = 0
    for i in range(len(inp) // 4 + 1):
        ax, ay = int(inp[4 * i][12:14]), int(inp[4 * i][18:])
        bx, by = int(inp[4 * i + 1][12:14]), int(inp[4 * i + 1][18:])
        x, y = int(inp[4 * i + 2][9:].split(", Y=")[0]), int(inp[4 * i + 2][9:].split(", Y=")[1])
        
        a0 = by * x - bx * y
        b0 = -ay * x + ax * y
        d = ax * by - bx * ay

        if d < 0:
            d *= -1
            a0 *= -1
            b0 *= -1

        if a0 < 0 or b0 < 0 \
        or a0 % d != 0 or b0 % d != 0:
            continue

        total += (3 * a0 + b0) // d
    return total

def main_part_2(inp: list[str]) -> int:
    total = 0
    for i in range(len(inp) // 4 + 1):
        ax, ay = int(inp[4 * i][12:14]), int(inp[4 * i][18:])
        bx, by = int(inp[4 * i + 1][12:14]), int(inp[4 * i + 1][18:])
        x, y = int(inp[4 * i + 2][9:].split(", Y=")[0]), int(inp[4 * i + 2][9:].split(", Y=")[1])
        x += 10000000000000
        y += 10000000000000
        
        a0 = by * x - bx * y
        b0 = -ay * x + ax * y
        d = ax * by - bx * ay

        if d < 0:
            d *= -1
            a0 *= -1
            b0 *= -1

        if a0 < 0 or b0 < 0 \
        or a0 % d != 0 or b0 % d != 0:
            continue

        total += (3 * a0 + b0) // d
    return total

def main() -> None:
    test_input = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""
    test_input_parsed = test_input.splitlines()
    test_output_part_1_expected = 480

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
