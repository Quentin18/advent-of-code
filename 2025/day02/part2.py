def is_valid_id(id_: int) -> bool:
    id_str = str(id_)
    id_length = len(id_str)

    for i in range(1, id_length // 2 + 1):
        if id_length % i != 0:
            continue

        if id_str.count(id_str[:i]) == id_length // i:
            return False

    return True


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        id_ranges = [id_range.strip() for id_range in file.read().split(",")]

    output = 0

    for id_range in id_ranges:
        left, right = id_range.split("-")
        for i in range(int(left), int(right) + 1):
            if not is_valid_id(i):
                output += i

    print(output)


if __name__ == "__main__":
    main()
