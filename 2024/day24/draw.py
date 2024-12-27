import graphviz

SWAPS = {
    "z08": "ffj",
    "z22": "gjh",
    "z31": "jdr",
    "kfm": "dwp",
}


def main() -> None:
    constant_constraints = {}
    operation_constraints = {}

    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file:
            if ":" in line:
                name, value = line.strip().split(": ")
                constant_constraints[name] = value

            elif "->" in line:
                value, name = line.strip().split(" -> ")
                operation_constraints[name] = value

    for left, right in SWAPS.items():
        operation_constraints[left], operation_constraints[right] = (
            operation_constraints[right],
            operation_constraints[left],
        )

    dot = graphviz.Digraph("FullAdder", format="png")
    dot.attr(rankdir="LR")

    operator_counters = {"AND": 0, "OR": 0, "XOR": 0}
    operator_colors = {"AND": "lightgreen", "OR": "orange", "XOR": "lightblue"}

    for result_name, constraint in sorted(operation_constraints.items()):
        lhs, operator, rhs = constraint.split()
        lhs, rhs = sorted((lhs, rhs))
        operator_name = f"{operator}{operator_counters[operator]}"
        dot.node(
            name=operator_name,
            label=operator,
            shape="rectangle",
            style="filled",
            color=operator_colors[operator],
        )
        dot.edge(lhs, operator_name)
        dot.edge(rhs, operator_name)
        dot.edge(operator_name, result_name)
        operator_counters[operator] += 1

    dot.render("full_adder_graph", view=True)


if __name__ == "__main__":
    main()
