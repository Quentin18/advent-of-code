import re


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        string = file.read().strip()

    matches = re.findall(r"mul\((\d+),(\d+)\)", string)

    print(sum(int(x) * int(y) for x, y in matches))


if __name__ == "__main__":
    main()
