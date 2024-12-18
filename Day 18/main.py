from __future__ import annotations
import os
from collections import *
from functools import *
from itertools import *
from math import *

from typing import *
from collections import deque


class State:
    def __init__(self, grid: list[list[str]], x: int, y: int) -> None:
        self.grid = grid
        self.x = x
        self.y = y

    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __lt__(self, other: State) -> bool:
        return hash(self) < hash(other)
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and hash(self) == hash(other)
    
    def get_children(self) -> list[State]:
        children = []

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = self.x + dx, self.y + dy
            
            if not (0 <= nx < len(self.grid)) \
            or not (0 <= ny < len(self.grid)) \
            or self.grid[ny][nx] == "#":
                continue

            children.append(State(self.grid, nx, ny))
        
        return children
    
    def finished(self) -> bool:
        return self.x == len(self.grid) - 1 and self.y == len(self.grid) - 1
    
    def solve(self) -> int:
        states: deque[tuple[int, State]] = deque()
        states.append((0, self))
        found: set[State] = set()

        while states:
            total_cost, state = states.popleft()

            if state.finished():
                return total_cost

            if state in found:
                continue

            found.add(state)

            for child in state.get_children():
                states.append((total_cost + 1, child))

        return -1

def main_part_1(inp: list[str], size: int = 71, tiles: int = 1024) -> int:
    grid = [["." for _ in range(size)] for _ in range(size)]
    for tile in inp[:tiles]:
        x, y = tuple(map(int, tile.split(",")))
        grid[y][x] = "#"
    
    return State(grid, 0, 0).solve()

def main_part_2(inp: list[str], size: int = 71) -> str:
    lb = 0
    ub = len(inp) - 1

    while lb <= ub:
        mid = (lb + ub) // 2
        if main_part_1(inp, size, mid) == -1:
            ub = mid - 1
        else:
            lb = mid + 1
        
    
    return inp[lb - 1]

def main() -> None:
    test_input = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""
    test_input_parsed = test_input.splitlines()
    test_output_part_1_expected = 22
    test_output_part_2_expected = "6,1"

    file_location = os.path.dirname(os.path.realpath(__file__))
    file_location = file_location + "/input.txt"
    with open(file_location, "r") as file:
        input_file = file.read().splitlines()

    test_output_part_1 = main_part_1(test_input_parsed, 7, 12)
    test_output_part_2 = main_part_2(test_input_parsed, 7)

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
