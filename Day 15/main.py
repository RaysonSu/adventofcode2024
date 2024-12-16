import os
from collections import *
from functools import *
from itertools import *
from math import *

def main_part_1(inp: list[str]) -> int:
    index = inp.index("")
    grid = list(map(list, inp[:index]))
    rules = "".join(inp[index:])
    y = [i for i, e, in enumerate(grid) if "@" in e][0]
    x = grid[y].index("@")
    grid[y][x] = "."

    for action in rules:
        match action:
            case "<":
                dx, dy = -1, 0
            case ">":
                dx, dy = 1, 0
            case "v":
                dx, dy = 0, 1
            case "^":
                dx, dy = 0, -1
        
        nx, ny = x + dx, y + dy

        if grid[ny][nx] == ".":
            x, y = nx, ny
            continue
        
        if grid[ny][nx] == "#":
            continue

        tnx, tny = nx, ny
        while grid[tny][tnx] == "O":
            tnx += dx
            tny += dy
        
        if grid[tny][tnx] == "#":
            continue

        grid[tny][tnx] = "O"
        grid[ny][nx] = "."
        x, y = nx, ny

    total = 0
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char == "O":
                total += 100 * i + j

    return total

def try_move(grid: list[list[str]], x: int, y: int, dx: int, dy: int) -> tuple[bool, set[tuple[int, int]]]:
    nx, ny = x + dx, y + dy
    
    new_tile = grid[ny][nx] # -> . or [ or ] or #

    if new_tile == "#":
        return False, set()
    
    moved = {(x, y)}

    left_moved: set[tuple[int, int]]
    right_moved: set[tuple[int, int]]

    left_valid, left_moved = True, set()
    right_valid, right_moved = True, set()

    match new_tile:
        case "[":
            if dx == -1:
                return True, moved

            left_valid, left_moved = try_move(grid, nx, ny, dx, dy)
            right_valid, right_moved = try_move(grid, nx + 1, ny, dx, dy)

            if not (left_valid and right_valid):
                return False, set()
            
            moved.update(left_moved, right_moved)
        case "]":
            if dx == 1:
                return True, moved

            left_valid, left_moved = try_move(grid, nx - 1, ny, dx, dy)
            right_valid, right_moved = try_move(grid, nx, ny, dx, dy)

            if not (left_valid and right_valid):
                return False, set()
            
            moved.update(left_moved, right_moved)

    return True, moved


def main_part_2(inp: list[str]) -> int:
    index = inp.index("")
    grid = [list(
        row
        .replace(".", "..")
        .replace("@", "@.")
        .replace("O", "[]")
        .replace("#", "##"))
        for row in inp[:index]]
    rules = "".join(inp[index:])
    y = [i for i, e, in enumerate(grid) if "@" in e][0]
    x = grid[y].index("@")
    
    for action in rules:
        match action:
            case "<":
                dx, dy = -1, 0
            case ">":
                dx, dy = 1, 0
            case "v":
                dx, dy = 0, 1
            case "^":
                dx, dy = 0, -1

        valid, moved = try_move(grid, x, y, dx, dy)

        if not valid: 
            continue

        data = {}
        for tx, ty in moved:
            data[(tx, ty)] = grid[ty][tx]
            grid[ty][tx] = "."
        
        for tx, ty in moved:
            grid[ty + dy][tx + dx] = data[(tx, ty)]
        
        grid[y][x] = "."

        x, y = x + dx, y + dy
    
    total = 0
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char == "[":
                total += 100 * i + j

    return total

def main() -> None:
    test_input = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""
    test_input_parsed = test_input.splitlines()
    test_output_part_1_expected = 10092
    test_output_part_2_expected = 9021

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
