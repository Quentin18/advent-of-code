import numpy as np


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        worksheet = np.array([list(line.replace("\n", "")) for line in file])

    total = 0
    symbol = None
    result = None

    for column in worksheet.T:
        if symbol is None:
            symbol = column[-1]
            result = 1 if symbol == "*" else 0

        number = "".join(column[:-1]).strip()

        if number:
            if symbol == "+":
                result += int(number)
            elif symbol == "*":
                result *= int(number)
        else:
            total += result
            symbol = None
            result = None

    total += result

    print(total)


if __name__ == "__main__":
    main()
