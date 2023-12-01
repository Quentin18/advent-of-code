import re


def main() -> None:
    values = []
    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file:
            numbers = re.sub("[^0-9]", "", line.strip())
            values.append(int(numbers[0] + numbers[-1]))
    response = sum(values)
    print(response)


if __name__ == "__main__":
    main()
