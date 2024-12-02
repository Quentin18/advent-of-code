import numpy as np


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        reports = [list(map(int, line.strip().split())) for line in file]

    safe = 0

    for report in reports:
        for i in range(len(report)):
            truncated_report = report[:i] + report[i + 1 :]
            differences = np.absolute(np.diff(truncated_report))
            if (
                (
                    truncated_report == sorted(truncated_report)
                    or truncated_report == sorted(truncated_report)[::-1]
                )
                and (differences >= 1).all()
                and (differences <= 3).all()
            ):
                safe += 1
                break

    print(safe)


if __name__ == "__main__":
    main()
