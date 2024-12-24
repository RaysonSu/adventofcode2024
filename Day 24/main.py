import os
from collections import *
from functools import *
from itertools import *
from math import *
from graphlib import TopologicalSorter

class Graph:
    def __init__(self, program: list[str]) -> None:
        self.vertices: set[str] = set()
        self.parents: dict[str, tuple[str, str, str]] = {}
        self.alias: dict[str, str] = {}

        for row in program:
            self.parents[row[-3:]] = (row[:3], row[-10:-7], row[4:7].strip())
            self.vertices.union({row[-3:], row[:3], row[-10:-7]})
    
    def make_dot_format(self) -> str:
        ret = "digraph {\n"
        for c, (p1, p2, op) in self.parents.items():
            color = {"OR": "red", "XOR": "blue", "AND": "green"}[op]
            ret += f"    {p1} -> {c} [color=\"{color}\"]\n"
            ret += f"    {p2} -> {c} [color=\"{color}\"]\n"
        ret += "}"

        return ret

    
    def create_alias(self, alias: str, original: str) -> None:
        self.alias[alias] = original

    def confirm(self, child: str, parent_1: str, parent_2: str, operation: str) -> bool:
        if child in self.alias:
            child = self.alias[child]
        
        if parent_1 in self.alias:
            parent_1 = self.alias[parent_1]
        
        if parent_2 in self.alias:
            parent_2 = self.alias[parent_2]

        return self.parents[child] == (parent_1, parent_2, operation) \
        or self.parents[child] == (parent_2, parent_1, operation, ) \
    
    def swap(self, vertex_1: str, vertex_2: str) -> None:
        if vertex_1 in self.alias:
            vertex_1 = self.alias[vertex_1]
        
        if vertex_2 in self.alias:
            vertex_2 = self.alias[vertex_2]

        self.parents[vertex_1], self.parents[vertex_2] = self.parents[vertex_2], self.parents[vertex_1]
    
    def get_child(self, parent_1: str, parent_2: str, operation: str) -> str:
        if parent_1 in self.alias:
            parent_1 = self.alias[parent_1]
        
        if parent_2 in self.alias:
            parent_2 = self.alias[parent_2]
        
        rule = (parent_1, parent_2, operation)
        rule_alt = (parent_2, parent_1, operation)

        for child, parent in self.parents.items():
            if parent == rule or parent == rule_alt:
                return child
        
        raise ValueError("No child.")
    
    def get_children_types(self, parent: str) -> tuple[int, int, int]:
        if parent in self.alias:
            parent = self.alias[parent]

        OR = 0
        XOR = 0
        AND = 0

        for rule in self.parents.values():
            if parent in rule:
                if rule[2] == "OR":
                    OR += 1
                elif rule[2] == "XOR":
                    XOR += 1
                elif rule[2] == "AND":
                    AND += 1
        
        return (OR, XOR, AND)


def main_part_1(inp: list[str]) -> int:
    data_split = inp.index("")
    data = inp[:data_split]
    program = inp[data_split+1:]

    values = {q[:3]: int(q[-1]) for q in data}

    actions = {row[-3:]: (row[:3], row[-10:-7], row[4:7]) for row in program}
    program_parsed = {result: args[:2] for result, args in actions.items()}

    ts = TopologicalSorter(program_parsed)
    for res in ts.static_order():
        if res not in program_parsed:
            continue

        arg1, arg2, operand = actions[res]

        match operand:
            case "XOR":
                values[res] = values[arg1] ^ values[arg2]
            case "OR ":
                values[res] = values[arg1] | values[arg2]
            case "AND":
                values[res] = values[arg1] & values[arg2]

    output = [res for res in actions if res.startswith("z")]
    output.sort(reverse=True)

    total = 0
    for bit in output:
        total *= 2
        total += values[bit]

    return total

def main_part_2(inp: list[str]) -> str:
    data_split = inp.index("")
    program = inp[data_split+1:]
    swaps: list[str] = []

    graph = Graph(program)

    # print(graph.make_dot_format())
    length = data_split // 2 + 1

    z00 = graph.get_child("x00", "y00", "XOR")
    c00 = graph.get_child("x00", "y00", "AND")

    graph.create_alias("c00", c00)

    if graph.get_children_types(z00) != (0, 0, 0):
        swaps.append(z00)
        swaps.append(c00)
        graph.swap(z00, c00)
    
    for i in range(1, length - 1):
        if i == 17:
            pass

        name = str(i).zfill(2)
        errors = []
        names = {}

        xi = "x" + name
        yi = "y" + name
        cp = "c" + str(i - 1).zfill(2)
        pi = "p" + name
        qi = "q" + name
        ri = "r" + name

        checks = [
            ("p", (xi, yi, "AND"), (1, 0, 0)),
            ("q", (xi, yi, "XOR"), (0, 1, 1)),
            ("r", (qi, cp, "AND"), (1, 0 ,0)),
            ("z", (qi, cp, "XOR"), (0, 0, 0)),
            ("c", (pi, ri, "OR"), (0, 1, 1))
        ]

        for node, source, req in checks:
            names[node] = graph.get_child(*source)

            if graph.get_children_types(names[node]) != req:
                errors.append(node)
            else:
                graph.create_alias(f"{node}{name}", names[node])
            
            if len(errors) >= 2:
                graph.swap(names[errors[0]], names[errors[1]])
                swaps.append(names[errors[0]])
                swaps.append(names[errors[1]])
                graph.create_alias(errors[0] + name, names[errors[1]])
                graph.create_alias(errors[1] + name, names[errors[0]])

                names[errors[0]], names[errors[1]] = names[errors[1]], names[errors[0]]
                errors = []

    return ",".join(sorted(swaps))
    
def main() -> None:
    test_input = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""
    test_input_parsed = test_input.splitlines()
    test_output_part_1_expected = 2024

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
