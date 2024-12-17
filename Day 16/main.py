from __future__ import annotations

import os
from collections import *
from functools import *
from itertools import *
from math import *
from typing import *
import heapq

class State:
    def __init__(self, grid: list[str], x: int, y: int, dx: int, dy: int):
        self.x = x
        self.y = y
        self.grid = grid
        self.dx, self.dy = dx, dy

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.dx, self.dy))
    
    def __lt__(self, other: State) -> bool:
        return hash(self) < hash(other)
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and hash(self) == hash(other)
    
    def get_children(self) -> Sequence[tuple[int, State]]:
        children = []

        nx, ny = self.x + self.dx, self.y + self.dy

        if self.grid[ny][nx] != "#":
            children.append((1, State(self.grid, nx, ny, self.dx, self.dy)))
        
        children.append((1000, State(self.grid, self.x, self.y, self.dy, -self.dx)))
        children.append((1000, State(self.grid, self.x, self.y, -self.dy, self.dx)))

        return children
    
    def solve(self) -> tuple[int, State] | tuple[Literal[-1], None]:
        states: list[tuple[int, State]] = [(0, self)]
        
        best_score: dict[State, int] = {}
        while states:
            total_cost, state = heapq.heappop(states)

            if state.grid[state.y][state.x] == "E":
                return total_cost, state
            
            # if state.y == 134 and state.x == 57:
            #     continue

            if state not in best_score:
                best_score[state] = total_cost
            elif best_score[state] <= total_cost:
                continue

            best_score[state] = total_cost

            for cost, child in state.get_children():
                if child in best_score and total_cost + cost >= best_score[child]:
                    continue

                heapq.heappush(states, (total_cost + cost, child))

        return -1, None

    def find_min_dist(self) -> dict[State, int]:
        states: list[tuple[int, State]] = [(0, self)]
        
        best_score: dict[State, int] = {}
        while states:
            total_cost, state = heapq.heappop(states)

            if state not in best_score:
                best_score[state] = total_cost
            elif best_score[state] <= total_cost:
                continue

            best_score[state] = total_cost

            if state.grid[state.y][state.x] == "E":
                continue

            for cost, child in state.get_children():
                if child in best_score and total_cost + cost >= best_score[child]:
                    continue

                heapq.heappush(states, (total_cost + cost, child))

        return best_score

def main_part_1(inp: list[str]) -> int:
    return State(inp, 1, len(inp) - 2, 1, 0).solve()[0]

def main_part_2(inp: list[str]) -> int:
    end = State(inp, 1, len(inp) - 2, 1, 0).solve()[1]
    if not end:
        return 0

    distances = State(inp, 1, len(inp) - 2, 1, 0).find_min_dist()

    data = {(state.x, state.y, -state.dx, -state.dy): dist for state, dist in distances.items()}

    points: set[tuple[int, int]] = set()
    current = [(end.x, end.y, -end.dx, -end.dy)]
    states: set[tuple[int, int, int, int]] = set()
    while current:
        x, y, dx, dy = current.pop(0)

        if (x, y, dx, dy) in states:
            continue

        points.add((x, y))
        states.add((x, y, dx, dy))
        
        if (x, y, dx, dy) not in data:
            continue
        
        children = []
        children.append((x + dx, y + dy, dx, dy))
        children.append((x, y, -dy, dx))
        children.append((x, y, dy, -dx))

        for child in children:
            if child in data \
            and (data[(x, y, dx, dy)] - data[child]) in [1, 1000]:
                current.append(child)

    # grid = [list(row.replace(".", " ")) for row in inp]
    # for x, y in points:
    #     grid[y][x] = "O"
    
    # for row in grid:
    #     print("".join(row))

    return len(points)

def main() -> None:
    test_input = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""
    test_input_parsed = test_input.splitlines()
    test_output_part_1_expected = 11048
    test_output_part_2_expected = 64

    file_location = os.path.dirname(os.path.realpath(__file__))
    file_location = file_location + "/input.txt"
    with open(file_location, "r") as file:
        input_file = file.read().splitlines()

    test_output_part_1 = main_part_1(test_input_parsed)
    test_output_part_2 = 64

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
