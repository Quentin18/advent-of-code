import math
import re


def get_combo_operand(operand: int, registers: dict[str, int]) -> int:
    if 0 <= operand <= 3:
        return operand

    if operand == 4:
        return registers["A"]

    if operand == 5:
        return registers["B"]

    if operand == 6:
        return registers["C"]

    raise ValueError(f"invalid operand: {operand}")


def main() -> None:
    registers = {}
    program = None

    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("Register"):
                name, value = re.match(
                    r"Register ([ABC]): (\d+)",
                    line.strip(),
                ).groups()
                registers[name] = int(value)
            elif line.startswith("Program"):
                program = list(map(int, line.strip().split(": ")[1].split(",")))

    instruction_pointer = 0
    output = []

    while instruction_pointer < len(program):
        opcode, operand = program[instruction_pointer], program[instruction_pointer + 1]

        if opcode == 0:
            registers["A"] = math.trunc(
                registers["A"]
                / (2 ** get_combo_operand(operand=operand, registers=registers))
            )
        elif opcode == 1:
            registers["B"] = registers["B"] ^ operand
        elif opcode == 2:
            registers["B"] = get_combo_operand(operand=operand, registers=registers) % 8
        elif opcode == 3 and registers["A"] != 0:
            instruction_pointer = operand
            continue
        elif opcode == 4:
            registers["B"] = registers["B"] ^ registers["C"]
        elif opcode == 5:
            output.append(get_combo_operand(operand=operand, registers=registers) % 8)
        elif opcode == 6:
            registers["B"] = math.trunc(
                registers["A"]
                / (2 ** get_combo_operand(operand=operand, registers=registers))
            )
        elif opcode == 7:
            registers["C"] = math.trunc(
                registers["A"]
                / (2 ** get_combo_operand(operand=operand, registers=registers))
            )

        instruction_pointer += 2

    print(",".join(str(i) for i in output))


if __name__ == "__main__":
    main()
