from __future__ import annotations

import os
from collections import *
from functools import *
from itertools import *
from math import *
from typing import *
import heapq

class State:
    def __init__(self, grid: list[str], x: int, y: int, horizontal: bool):
        self.x = x
        self.y = y
        self.grid = grid
        self.horizontal = horizontal

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.horizontal))
    
    def __lt__(self, other: State) -> bool:
        return hash(self) < hash(other)
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and hash(self) == hash(other)
    
    def get_children(self) -> Sequence[tuple[int, State]]:
        children = []

        for delta in [-1, 1]:
            if self.horizontal:
                nx, ny = self.x + delta, self.y
            else:
                nx, ny = self.x, self.y + delta

            if self.grid[ny][nx] == "#":
                continue

            new_state = State(self.grid, nx, ny, self.horizontal)
            
            children.append((1, new_state))
        
        children.append((1000, State(self.grid, self.x, self.y, not self.horizontal)))

        return children
    
    def finished(self) -> bool:
        return self.grid[self.y][self.x] == "E"
    
    def solve(self) -> tuple[int, State] | tuple[Literal[-1], None]:
        '''A function that finds the mininum distance to a target node.'''
        states: list[tuple[int, State]] = [(0, self)]
        best_score: dict[State, int] = {}
        while states:
            total_cost, state = heapq.heappop(states)

            if state.finished():
                return total_cost, state

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
        '''A function that finds the mininum distance to all possible states.'''
        states: list[tuple[int, State]] = [(0, self)]
        best_score: dict[State, int] = {}
        while states:
            total_cost, state = heapq.heappop(states)

            if state not in best_score:
                best_score[state] = total_cost
            elif best_score[state] <= total_cost:
                continue

            best_score[state] = total_cost

            if state.finished():
                continue

            for cost, child in state.get_children():
                if child in best_score and total_cost + cost >= best_score[child]:
                    continue

                heapq.heappush(states, (total_cost + cost, child))

        return best_score

def main_part_1(inp: list[str]) -> int:
    return State(inp, 1, len(inp) - 2, True).solve()[0]

def main_part_2(inp: list[str]) -> int:
    distances = State(inp, 1, len(inp) - 2, True).find_min_dist()
    end = State(inp, 1, len(inp) - 2, True).solve()[1]

    if not end:
        return 0

    data = {(state.x, state.y, state.horizontal): dist for state, dist in distances.items()}

    points: set[tuple[int, int]] = set()
    current = [(end.x, end.y, end.horizontal)]
    states: set[tuple[int, int, bool]] = set()
    while current:
        x, y, d = current.pop(0)

        if (x, y, d) in states:
            continue

        points.add((x, y))
        states.add((x, y, d))

        if (x, y) == (1, 5):
            pass
        
        if (x, y, d) not in data:
            continue

        score = data[(x, y, d)]
        children = []
        for delta in [-1, 1]:
            if d:
                nx, ny = x + delta, y
            else:
                nx, ny = x, y + delta
            
            children.append((nx, ny, d))
        
        children.append((x, y, not d))

        for nx, ny, nd in children:
            if (nx, ny, nd) in data and data[(nx, ny, nd)] < score:
                current.append((nx, ny, nd))
    
    # grid = [list(row) for row in inp]
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
