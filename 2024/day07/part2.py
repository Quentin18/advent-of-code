import itertools

OPERATORS = ("+", "*", "||")


def is_solvable(result: int, values: list[int]) -> bool:
    for operators in itertools.product(OPERATORS, repeat=len(values) - 1):
        r = values[0]
        for value, operator in zip(values[1:], operators):
            if operator == "+":
                r += value
            elif operator == "*":
                r *= value
            elif operator == "||":
                r = int(str(r) + str(value))
            else:
                raise RuntimeError(f"unknown operator {operator}")

        if result == r:
            return True

    return False


def main() -> None:
    equations = {}

    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file:
            result, values = line.strip().split(": ")
            equations[int(result)] = list(map(int, values.split()))

    total_calibration_result = sum(
        result
        for result, values in equations.items()
        if is_solvable(result=result, values=values)
    )
    print(total_calibration_result)


if __name__ == "__main__":
    main()
