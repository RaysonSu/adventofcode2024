import os
from collections import *
from functools import *
from itertools import *
from math import *

class Graph:
    def __init__(self, vertices: set[str], edges: dict[str, set[str]]) -> None:
        self.vertices = vertices
        self.edges = edges
    
    def _find_max_clique(self, required: set[str], possible: set[str], excluded: set[str]) -> set[str]:
        if not possible and not excluded:
            return required
        
        max_clique: set[str] = set()

        for vertex in possible:
            neighbours = self.edges[vertex]
            found_clique = self._find_max_clique(
                required.union({vertex}), 
                possible.intersection(neighbours), 
                excluded.intersection(neighbours)
            )

            if len(found_clique) > len(max_clique):
                max_clique = found_clique
            
            possible = possible.difference({vertex})
            excluded = excluded.union({vertex})

            if len(max_clique) >= len(possible):
                break
    
        return max_clique

    def find_max_clique(self) -> set[str]:
        return self._find_max_clique(set(), self.vertices, set())

def parse_edges(vertices: set[str], edges: set[tuple[str, ...]]) -> dict[str, set[str]]:
    ret: dict[str, set[str]] = {edge: set() for edge in vertices}
    for start, end, *_ in edges:
        ret[start].add(end)
        ret[end].add(start)
    
    return ret

def main_part_1(inp: list[str]) -> int:
    vertices = set("-".join(inp).split("-"))
    edges = parse_edges(vertices, set(map(lambda row: tuple(row.split("-")), inp)))

    t_vertices = {vertex for vertex in vertices if vertex[0] == "t"}
    
    total = 0
    for vt in t_vertices:
        for v1, v2 in combinations(edges[vt], 2):
            for vl, vh in pairwise(v for v in (vt, v1, v2) if v[0] == "t"):
                if vl > vh:
                    break
            else:
                if v2 in edges[v1]:
                    total += 1
    
    return total


def main_part_2(inp: list[str]) -> str:
    vertices = set("-".join(inp).split("-"))
    edges = parse_edges(vertices, set(map(lambda row: tuple(row.split("-")), inp)))

    graph = Graph(vertices, edges)
    
    return ",".join(sorted(graph.find_max_clique()))

def main() -> None:
    test_input = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""
    test_input_parsed = test_input.splitlines()
    test_output_part_1_expected = 7
    test_output_part_2_expected = "co,de,ka,ta"

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
