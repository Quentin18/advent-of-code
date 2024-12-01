def main() -> None:
    first_list = []
    second_list = []

    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file:
            i, j = line.strip().split()
            first_list.append(int(i))
            second_list.append(int(j))

    score = 0
    for i in first_list:
        score += i * second_list.count(i)

    print(score)


if __name__ == "__main__":
    main()
