import numpy as np


def count_vertical_reflection(pattern: np.ndarray) -> int:
    for col in range(1, pattern.shape[1]):
        if (
            col <= pattern.shape[1] / 2
            and (pattern[:, :col] == np.fliplr(pattern[:, col : 2 * col])).all()
        ):
            return col

        if (
            col > pattern.shape[1] / 2
            and (
                pattern[:, (2 * col - pattern.shape[1]) : col]
                == np.fliplr(pattern[:, col:])
            ).all()
        ):
            return col

    return 0


def main() -> None:
    patterns = []
    pattern = []

    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                patterns.append(np.array(pattern))
                pattern = []
            else:
                pattern.append(list(line.strip()))

        patterns.append(np.array(pattern))

    left_cols = 0
    up_rows = 0
    for pattern in patterns:
        left_cols += count_vertical_reflection(pattern=pattern)
        up_rows += count_vertical_reflection(pattern=pattern.T)

    response = left_cols + 100 * up_rows
    print(response)


if __name__ == "__main__":
    main()
