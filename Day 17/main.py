import os
from collections import *
from functools import *
from itertools import *
from math import *

def run_program(program: list[int], a: int, b: int, c: int) -> list[int]:
    ip = 0
    output = []

    while ip < len(program) - 1:
        opcode = program[ip]
        operand = program[ip + 1]
        coperand = 0
        match operand:
            case 0 | 1 | 2 | 3:
                coperand = operand
            case 4:
                coperand = a
            case 5:
                coperand = b
            case 6:
                coperand = c

        match opcode:
            case 0:
                a //= 2 ** coperand
            case 1:
                b ^= operand
            case 2:
                b = coperand % 8
            case 3:
                if a != 0:
                    ip = operand - 2
            case 4:
                b ^= c
            case 5:
                output.append(coperand % 8)
            case 6:
                b = a // 2 ** coperand
            case 7:
                c = a // 2 ** coperand
        
        ip += 2

    return output

def main_part_1(inp: list[str]) -> str:
    a, b, c = int(inp[0][11:]), int(inp[1][11:]), int(inp[2][11:])
    program = eval("[" + inp[-1][9:] + "]")
    
    return ",".join(map(str, run_program(program, a, b, c)))

def main_part_2(inp: list[str]) -> int:
    program = eval("[" + inp[-1][9:] + "]")

    guess = [0]
    while True:
        value = reduce(lambda a, b: (a << 3) + b, guess)
        result = run_program(program, value, 0, 0)
        
        if result[-len(guess):] != program[-len(guess):]:
            while guess[-1] == 7:
                guess.pop()
            
            guess[-1] += 1
        elif result == program:
            return value
        else:
            guess.append(0)


def main() -> None:
    test_input = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""
    test_input_parsed = test_input.splitlines()
    test_output_part_1_expected = "5,7,3,0"

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
