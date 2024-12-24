import z3


def main() -> None:
    constraints = {}
    z_names = []

    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file:
            if ":" in line:
                name, value = line.strip().split(": ")
                constraints[name] = value

            elif "->" in line:
                value, name = line.strip().split(" -> ")
                value = value.replace("AND", "&").replace("XOR", "^").replace("OR", "|")
                constraints[name] = value
                if name.startswith("z"):
                    z_names.append(name)

    z_names.sort()
    z_variables = []

    for name in sorted(constraints):
        if name in z_names:
            z_variables.append(z3.BitVec(name, 64))
            globals()[name] = z_variables[-1]
        else:
            globals()[name] = z3.BitVec(name, 64)

    solver = z3.Solver()

    for name, value in constraints.items():
        solver.add(eval(f"{name} == {value}"))  # pylint: disable=eval-used

    if solver.check() == z3.sat:
        model = solver.model()
        print(int("".join(model[i].as_string() for i in z_variables[::-1]), 2))


if __name__ == "__main__":
    main()
