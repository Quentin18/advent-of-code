import numpy as np


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        matrix = []
        symbols = None

        for line in file:
            if "*" in line:
                symbols = line.strip().replace(" ", "")
            else:
                matrix.append([int(i.strip()) for i in line.strip().split()])

    assert symbols is not None
    matrix = np.array(matrix, dtype=int)

    total = sum(
        matrix[:, i].sum() if symbol == "+" else matrix[:, i].prod()
        for i, symbol in enumerate(symbols)
    )
    print(total)


if __name__ == "__main__":
    main()
