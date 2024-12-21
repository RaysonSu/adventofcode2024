import os
from collections import *
from functools import *
from itertools import *
from math import *

# i can't come up with a better way of doing this....
def get_moves(start: str, end: str) -> str:
    return {
        "A": {"A": "A",    "^": "<A",  "<": "v<<A", ">": "vA",  "v": "<vA"}, 
        "^": {"A": ">A",   "^": "A",   "<": "v<A",  ">": "v>A", "v": "vA"}, 
        "<": {"A": ">>^A", "^": ">^A", "<": "A",    ">": ">>A", "v": ">A"}, 
        ">" :{"A": "^A",   "^": "<^A", "<": "<<A",  ">": "A",   "v": "<A"}, 
        "v": {"A": "^>A",  "^": "^A",  "<": "<A",   ">": ">A",  "v": "A"}
    }[start][end]

def get_move_numpad_options(start: str, end: str) -> list[str]:
    buttons = {
                     "0": (1, 3), "A": (2, 3),
        "1": (0, 2), "2": (1, 2), "3": (2, 2),
        "4": (0, 1), "5": (1, 1), "6": (2, 1),
        "7": (0, 0), "8": (1, 0), "9": (2, 0)
    }

    sx, sy = buttons[start]
    ex, ey = buttons[end]

    dx = ex - sx
    dy = ey - sy

    horizontal = (">" if dx > 0 else "<") * abs(dx)
    vertical = ("^" if dy < 0 else "v") * abs(dy)

    options = []
    if (ex, sy) != (0, 3):
        options.append(horizontal + vertical + "A")
    
    if (sx, ey) != (0, 3):
        options.append(vertical + horizontal + "A")

    return options

def get_complexity(code: str, layer: int) -> int:
    options = [get_move_numpad_options(start, end) for start, end in zip("A" + code, code)]
    shortest = 1 << 1024

    for option in product(*options):
        base_code = "".join(option)
        moves = Counter(zip("A" + base_code, base_code))

        for _ in range(layer):
            new_moves: Counter[tuple[str, str]] = Counter()
            for (start, end), amount in moves.items():
                actions = get_moves(start, end)
                for s, e in zip("A" + actions, actions):
                    new_moves[(s, e)] += amount
            moves = new_moves
        
        shortest = min(shortest, sum(moves.values()))

    return shortest * int(code[:-1])

def main_part_1(inp: list[str]) -> int:
    return sum([get_complexity(code, 2) for code in inp])

def main_part_2(inp: list[str]) -> int:
    return sum([get_complexity(code, 25) for code in inp])

def main() -> None:
    test_input = """029A
980A
179A
456A
379A"""
    test_input_parsed = test_input.splitlines()
    test_output_part_1_expected = 126384

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
