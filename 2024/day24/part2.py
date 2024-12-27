# pylint: disable=too-many-branches
# https://www.reddit.com/r/adventofcode/comments/1hl698z/comment/m3k68gd/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button

import sys

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

    xy_xor_output = set()
    other_xor_operands = set()

    for output, constraint in operation_constraints.items():
        a, op, b = constraint.split()
        a, b = sorted((a, b))

        # check all gates that output z__ must be XOR except for z45
        if output[0] == "z" and output != "z45" and op != "XOR":
            print(
                f"{constraint} outputs {output} but is not XOR",
                file=sys.stderr,
            )
            continue

        if op != "XOR":
            continue

        # check x00 XOR y00 -> z00
        if a == "x00" and b == "y00":
            if output != "z00":
                print(
                    f"{constraint} must output z00, got {output}",
                    file=sys.stderr,
                )
            continue

        # check x__ XOR y__ gates do not output z__
        if a[0] == "x" and b[0] == "y":
            xy_xor_output.add(output)
            if output[0] == "z":
                print(
                    f"{constraint} must not output z__, got {output}",
                    file=sys.stderr,
                )
            continue

        other_xor_operands.add((a, b))

        # check other XOR gates output z__
        if output[0] != "z":
            print(
                f"{constraint} must output z__, got {output}",
                file=sys.stderr,
            )
            continue

    for output in xy_xor_output:
        if all(output not in operands for operands in other_xor_operands):
            print(
                f"{output} must be in other XOR gate",
                file=sys.stderr,
            )

    def evaluate(constraint_name: str) -> str:
        if constraint_name in constant_constraints:
            return constraint_name

        a, op, b = operation_constraints[constraint_name].split()
        return f"({evaluate(a)} {op} {evaluate(b)})"

    for z_bit in sorted(name for name in operation_constraints if name[0] == "z"):
        z_bit_number = int(z_bit[1:])
        equation = evaluate(z_bit)
        if (
            z_bit != "z45"
            and f"x{z_bit_number:02} XOR y{z_bit_number:02}" not in equation
            and f"y{z_bit_number:02} XOR x{z_bit_number:02}" not in equation
        ):
            print(
                f"{z_bit} does not contain x{z_bit_number:02} XOR y{z_bit_number:02}",
                file=sys.stderr,
            )

    print(",".join(sorted((*SWAPS.keys(), *SWAPS.values()))))


if __name__ == "__main__":
    main()
