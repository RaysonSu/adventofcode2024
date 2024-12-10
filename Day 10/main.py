from __future__ import annotations

import os
from collections import *
from functools import *
from itertools import *
from math import *

class State():
    def __init__(self, grid: list[list[int]], x: int, y: int) -> None:
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
        children: list[State] = []
        current_value = self.grid[self.y][self.x]
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx = self.x + dx
            ny = self.y + dy

            if not (0 <= nx < len(self.grid[0]) \
                    and 0 <= ny < len(self.grid)):
                continue
            
            if self.grid[ny][nx] != current_value + 1:
                continue
            
            children.append(State(self.grid, nx, ny))
        
        return children
    
    def finished(self) -> bool:
        return self.grid[self.y][self.x] == 9

    def get_score(self) -> int:
        '''A function that finds the mininum distance to a target node.'''
        states: deque[tuple[int, State]] = deque()
        states.append((0, self))
        found: set[State] = set()

        while states:
            total_cost, state = states.popleft()

            if state in found:
                continue

            found.add(state)

            for child in state.get_children():
                states.append((total_cost + 1, child))

        total = 0
        for state in found:
            if state.finished():
                total += 1
        
        return total

    def get_ranking(self) -> int:
        if self.finished():
            return 1
        
        total = 0

        for child in self.get_children():
            total += child.get_ranking()
        
        return total


def main_part_1(inp: list[str]) -> int:
    grid = [[int(char) for char in row] for row in inp]
    total = 0
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if val == 0:
                total += State(grid, x, y).get_score()

    return total

def main_part_2(inp: list[str]) -> int:
    grid = [[int(char) for char in row] for row in inp]
    total = 0
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if val == 0:
                total += State(grid, x, y).get_ranking()

    return total

def main() -> None:
    test_input = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""
    test_input_parsed = test_input.splitlines()
    test_output_part_1_expected = 36
    test_output_part_2_expected = 81

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
