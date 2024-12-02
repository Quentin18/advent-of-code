import numpy as np


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        reports = [list(map(int, line.strip().split())) for line in file]

    safe = 0

    for report in reports:
        differences = np.absolute(np.diff(report))
        if (
            (report == sorted(report) or report == sorted(report)[::-1])
            and (differences >= 1).all()
            and (differences <= 3).all()
        ):
            safe += 1

    print(safe)


if __name__ == "__main__":
    main()
