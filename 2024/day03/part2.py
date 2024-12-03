import re


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        string = file.read().strip()

    dont_index = -2
    do_index = -1
    while dont_index < do_index:
        dont_index = string.find("don't()")
        do_index = string.find("do()", dont_index)
        string = string[:dont_index] + string[do_index:]

    matches = re.findall(r"mul\((\d+),(\d+)\)", string)

    print(sum(int(x) * int(y) for x, y in matches))


if __name__ == "__main__":
    main()
