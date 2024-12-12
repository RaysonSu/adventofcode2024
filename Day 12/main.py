from __future__ import annotations

import os
from collections import *
from functools import *
from itertools import *
from math import *

class State():
    def __init__(self, grid: list[str], x: int, y: int) -> None:
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
            
            if self.grid[ny][nx] != current_value:
                continue
            
            children.append(State(self.grid, nx, ny))
        
        return children
    
    def finished(self) -> bool:
        return True

    def find_region(self) -> tuple[set[tuple[int, int]], int]:
        states: deque[tuple[int, State]] = deque()
        states.append((0, self))
        found: set[State] = set()
        edges: int = 0

        while states:
            total_cost, state = states.popleft()

            if state in found:
                continue

            found.add(state)

            children = state.get_children()

            for child in children:
                states.append((total_cost + 1, child))
            
            edges += 4 - len(children)

        total = 0
        for state in found:
            if state.finished():
                total += 1
        
        return set(map(lambda x: (x.x, x.y), found)), edges

def count_sides(region: set[tuple[int, int]]) -> int:
    corner_canidates: set[tuple[int, int]] = set()
    for x, y in region:
        corner_canidates.add((x, y))
        corner_canidates.add((x + 1, y))
        corner_canidates.add((x, y + 1))
        corner_canidates.add((x + 1, y + 1))

    total = 0

    for x, y in corner_canidates:
        counter = 0
        # 1|2
        # -+-
        # 3|4
        #                  1        2        3       4
        for dx, dy in [(-1, -1), (0, -1), (-1, 0), (0, 0)]:
            counter *= 2
            if (x + dx, y + dy) in region:
                counter += 1
        
        if counter in [0b0001, 0b0010, 0b0100, 0b1000, 0b1110, 0b1101, 0b1011, 0b0111]:
            total += 1
        
        if counter in [0b1001, 0b0110]:
            total += 2
    
    return total

def main_part_1(inp: list[str]) -> int:
    seen: set[tuple[int, int]] = set()
    total = 0
    for x in range(len(inp[0])):
        for y in range(len(inp)):
            if (x, y) in seen:
                continue

            tiles, edges = State(inp, x, y).find_region()
            seen = seen.union(tiles)
            total += len(tiles) * edges
    
    return total


def main_part_2(inp: list[str]) -> int:
    seen: set[tuple[int, int]] = set()
    total = 0
    for x in range(len(inp[0])):
        for y in range(len(inp)):
            if (x, y) in seen:
                continue

            tiles, _ = State(inp, x, y).find_region()
            total += len(tiles) * count_sides(tiles)

            seen = seen.union(tiles)
    
    return total

def main() -> None:
    test_input = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""
    test_input_parsed = test_input.splitlines()
    test_output_part_1_expected = 1930
    test_output_part_2_expected = 1206 

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
