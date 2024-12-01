import numpy as np


def main() -> None:
    first_list = []
    second_list = []

    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file:
            i, j = line.strip().split()
            first_list.append(int(i))
            second_list.append(int(j))

    first_list.sort()
    second_list.sort()

    distances = np.absolute(np.array(first_list) - np.array(second_list))
    print(distances.sum())


if __name__ == "__main__":
    main()
