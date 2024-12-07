import os
from collections import *
from functools import *
from itertools import *
from math import *

def find_locations(grid: list[str]) -> tuple[bool, set[tuple[int, int]]]:
    locations_seen: set[tuple[int, int]] = set()
    states_seen: set[tuple[int, int, int, int]] = set()
    
    if "^" not in "".join(grid):
        return False, locations_seen

    width = len(grid[0])
    height = len(grid)
    index = "".join(grid).index("^")
    x = index % width
    y = index // width
    dx = 0
    dy = -1

    while True:
        locations_seen.add((x, y))
        states_seen.add((x, y, dx, dy))
        x += dx
        y += dy

        if x < 0 or x >= width:
            break

        if y < 0 or y >= height:
            break

        if grid[y][x] == "#":
            x -= dx
            y -= dy
            dx, dy = -dy, dx
        
        if (x, y, dx, dy) in states_seen:
            return False, locations_seen
    
    return True, locations_seen

def main_part_1(inp: list[str]) -> int:
    return len(find_locations(inp)[1])

def main_part_2(inp: list[str]) -> int:
    total = 0

    for x, y in find_locations(inp)[1]:
        if inp[y][x] == "^":
            continue

        temp_list = inp.copy()
        temp_list[y] = temp_list[y][:x] \
                    + "#" \
                    + temp_list[y][x + 1:]

        if not find_locations(temp_list)[0]:
            total += 1
    
    return total

def main() -> None:
    test_input = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""
    test_input_parsed = test_input.splitlines()
    test_output_part_1_expected = 41
    test_output_part_2_expected = 6

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
