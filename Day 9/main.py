import os
from collections import *
from functools import *
from itertools import *
from math import *

def main_part_1(inp: list[str]) -> int:
    if len(inp[0]) % 2 == 0:
        inp[0] = inp[0][:-1]

    files_remaining = deque(map(list, enumerate(map(int, inp[0]))))
    
    adding_front = True
    total = 0
    index = 0

    while len(files_remaining) > 1:
        if adding_front:
            if files_remaining[0][1] == 0:
                adding_front = False
            else:
                total += files_remaining[0][0] // 2 * index
                index += 1
                files_remaining[0][1] -= 1
        else:
            if files_remaining[1][1] == 0:
                files_remaining.popleft()
                files_remaining.popleft()
                adding_front = True
            elif files_remaining[-1][1] == 0:
                files_remaining.pop()
                files_remaining.pop()
            else:
                total += files_remaining[-1][0] // 2 * index
                index += 1
                files_remaining[-1][1] -= 1
                files_remaining[1][1] -= 1
    
    if files_remaining:
        value, remaining = tuple(files_remaining.pop())
        for _ in range(remaining):
            total += value // 2 * index
            index += 1
    
    return total

def main_part_2(inp: list[str]) -> int:
    if len(inp[0]) % 2 == 0:
        inp[0] = inp[0][:-1]

    files: list[tuple[int, int]] = []
    holes: list[int] = []

    for index, size in enumerate(map(int, inp[0])):
        if index % 2 == 0:
            files.append((index // 2, size))
        else:
            holes.append(size)
            

    for file_index in range(len(files) - 1, -1, -1):
        file_location_index, file_size = \
            next(((f_location, f_size) 
                  for f_location, (f_index, f_size)
                  in enumerate(files)
                  if f_index == file_index))

        
        hole_location_index, hole_size = \
            next(((h_location, h_size)
                  for h_location, h_size
                  in enumerate(holes[:file_location_index])
                  if h_size >= file_size), (-1, -1))

        if hole_size == -1:
            continue

        # remove file
        files.pop(file_location_index)
        remvoed_hole_size = holes.pop(file_location_index - 1)

        if file_location_index != len(files):
            holes[file_location_index - 1] += remvoed_hole_size + file_size

        # put file back
        files.insert(hole_location_index + 1, (file_index, file_size))
        holes[hole_location_index] -= file_size
        holes.insert(hole_location_index, 0)


    index = 0
    total = 0
    for file_data, hole_size in zip_longest(files, holes):
        if file_data:
            file_index, file_size = file_data
            total += file_index * (index * file_size + file_size * (file_size - 1) // 2)
            index += file_size
        
        if hole_size:
            index += hole_size

    return total

# def main_part_2(inp: list[str]) -> int:
#     if len(inp[0]) % 2 == 0:
#         inp[0] = inp[0][:-1]

#     n = list(enumerate(map(int, inp[0])))
    
#     numbers = []
#     for i, v in n:
#         if i % 2 == 0:
#             numbers.append((i // 2, v))
#         else:
#             numbers.append((-1, v))

#     for i in range(len(n) // 2, -1, -1):
#         # print(i)
#         for j, (vb, sb) in enumerate(numbers):
#             if vb == i:
#                 index = j
#                 break
        
#         for k in range(index):
#             v, s = numbers[k]
#             if v == -1 and s >= sb:
#                 numbers.pop(index)
#                 numbers.insert(index, (-1, sb))
#                 numbers.pop(k)
#                 numbers.insert(k, (-1, s - sb))
#                 numbers.insert(k, (vb, sb))
#                 break
        
#         nnubers = [numbers[0]]
#         for x, y in numbers[1:]:
#             if x == nnubers[-1][0]:
#                 x, t = nnubers.pop()
#                 nnubers.append((x, y + t))
#             else:
#                 nnubers.append((x, y))
        
#         numbers = nnubers

#     nt = []
#     for p, q in numbers:
#         for _ in range(q):
#             nt.append(p)


#     return sum([i * v for i, v in enumerate(nt) if v != -1])
def main() -> None:
    test_input = """2333133121414131402"""
    test_input_parsed = test_input.splitlines()
    test_output_part_1_expected = 1928
    test_output_part_2_expected = 2858

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
