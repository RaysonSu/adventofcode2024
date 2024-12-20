from __future__ import annotations

import os
from collections import *
from functools import *
from itertools import *
from math import *

class State:
    def __init__(self, grid: list[str], x: int, y: int) -> None:
        self.grid = grid
        self.x = x
        self.y = y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return str((self.x, self.y))
    
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
    
    def find_min_dist(self) -> dict[tuple[int, int], int]:
        states: deque[tuple[int, State]] = deque()
        states.append((0, self))
        best_score: dict[State, int] = {}

        while states:
            total_cost, state = states.popleft()

            if state not in best_score:
                best_score[state] = total_cost
            elif best_score[state] <= total_cost:
                continue

            best_score[state] = total_cost

            for child in state.get_children():
                states.append((total_cost + 1, child))
        
        return {(state.x, state.y): score for state, score in best_score.items()}

    def max_solve(self, time_saved: int, max_cheats: int) -> int:
        total = 0;
        times = self.find_min_dist()

        for sx, sy in product(range(len(self.grid)), repeat=2):
            if self.grid[sy][sx] == "#":
                continue

            s_time = times[(sx, sy)]

            for dx in range(-max_cheats, max_cheats + 1):
                for dy in range(-max_cheats + abs(dx), max_cheats + 1 - abs(dx)):
                    ex, ey = sx + dx, sy + dy

                    
                    if not (0 <= ex < len(self.grid)) \
                    or not (0 <= ey < len(self.grid)):
                        continue

                    if self.grid[ey][ex] == "#":
                        continue

                    if times[(ex, ey)] - s_time - abs(dx) - abs(dy) >= time_saved:
                        total += 1
        
        return total

def main_part_1(inp: list[str], time_save: int = 100) -> int:
    y = [i for i, row in enumerate(inp) if "S" in row][0]
    x = inp[y].index("S")
    
    return State(inp, x, y).max_solve(time_save, 2)

def main_part_2(inp: list[str], time_save: int = 100) -> int:
    y = [i for i, row in enumerate(inp) if "S" in row][0]
    x = inp[y].index("S")

    return State(inp, x, y).max_solve(time_save, 20)

def main() -> None:
    test_input = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""
    test_input_parsed = test_input.splitlines()
    test_output_part_1_expected = 5
    test_output_part_2_expected = 41

    file_location = os.path.dirname(os.path.realpath(__file__))
    file_location = file_location + "/input.txt"
    with open(file_location, "r") as file:
        input_file = file.read().splitlines()

    test_output_part_1 = main_part_1(test_input_parsed, 20)
    test_output_part_2 = main_part_2(test_input_parsed, 70)

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
