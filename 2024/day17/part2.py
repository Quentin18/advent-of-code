import sys

import z3


def main() -> None:
    program = [2, 4, 1, 2, 7, 5, 0, 3, 4, 7, 1, 7, 5, 5, 3, 0]

    solver = z3.Solver()
    a_init = z3.BitVec("a", 49)
    a = a_init

    for i in program:
        b = a & 7  # a % 8
        b = b ^ 2  # (a % 8) XOR 2
        c = a >> b  # a // (2**((a % 8) XOR 2))
        a = a >> 3
        b = b ^ c  # ((a % 8) XOR 2) XOR (a // (2**((a % 8) XOR 2)))
        b = b ^ 7  # (((a % 8) XOR 2) XOR (a // (2**((a % 8) XOR 2)))) XOR 7
        out = b & 7  # ((((a % 8) XOR 2) XOR (a // (2**((a % 8) XOR 2)))) XOR 7) % 8
        solver.add(out == i)

    solver.add(a == 0)

    min_solution = None
    while solver.check() == z3.sat:
        model = solver.model()
        print(model, file=sys.stderr)
        solution = model[a_init].as_long()  # pylint: disable=no-member

        if min_solution is None or solution < min_solution:
            min_solution = solution

        solver.add(a_init < solution)

    print(min_solution)


if __name__ == "__main__":
    main()
