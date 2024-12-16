import os
from collections import *
from functools import *
from itertools import *
from math import *

def calculate_product(robot_data: list[tuple[tuple[int, int], tuple[int, int]]], time: int, width: int = 101, height: int = 103) -> int:
    cx = width // 2
    cy = height // 2
    
    quadrant_count = [0, 0, 0, 0]
    for position, velocity in robot_data:
        x = (position[0] + velocity[0] * time) % width
        y = (position[1] + velocity[1] * time) % height 

        if x < cx:
            if y < cy:
                quadrant_count[0] += 1
            elif y > cy:
                quadrant_count[1] += 1
        elif x > cx:
            if y < cy:
                quadrant_count[2] += 1
            elif y > cy:
                quadrant_count[3] += 1
    
    total = 1
    for count in quadrant_count:
        total *= count

    return total

def main_part_1(inp: list[str], width: int = 101, height: int = 103) -> int:
    robot_data: list[tuple[tuple[int, int], tuple[int, int]]] = []
    for row in inp:
        row_data = row.split(" ")
        position_data = row_data[0][2:].split(",")
        velocity_data = row_data[1][2:].split(",")
        position = (int(position_data[0]), int(position_data[1]))
        velocity = (int(velocity_data[0]), int(velocity_data[1]))
        robot_data.append((position, velocity))
    
    return calculate_product(robot_data, 100, width, height)



def main_part_2(inp: list[str], width: int = 101, height: int = 103) -> int:
    robot_data: list[tuple[tuple[int, int], tuple[int, int]]] = []
    for row in inp:
        row_data = row.split(" ")
        position_data = row_data[0][2:].split(",")
        velocity_data = row_data[1][2:].split(",")
        position = (int(position_data[0]), int(position_data[1]))
        velocity = (int(velocity_data[0]), int(velocity_data[1]))
        robot_data.append((position, velocity))
    
    time_points = [(calculate_product(robot_data, t, width, height), t) for t in range(width * height)]
    time_points.sort()

    return time_points[0][1]

def main() -> None:
    test_input = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""
    test_input_parsed = test_input.splitlines()
    test_output_part_1_expected = 12

    file_location = os.path.dirname(os.path.realpath(__file__))
    file_location = file_location + "/input.txt"
    with open(file_location, "r") as file:
        input_file = file.read().splitlines()

    test_output_part_1 = main_part_1(test_input_parsed, 11, 7)

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
