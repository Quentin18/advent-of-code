def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        disk_map = list(map(int, file.read().strip()))

    blocks = []
    for i, value in enumerate(disk_map):
        blocks.extend([i // 2 if i % 2 == 0 else -1] * value)

    left_index = 0
    right_index = len(blocks) - 1
    while left_index < right_index:
        while blocks[left_index] != -1 and left_index < right_index:
            left_index += 1

        while blocks[right_index] == -1 and right_index > left_index:
            right_index -= 1

        blocks[left_index], blocks[right_index] = (
            blocks[right_index],
            blocks[left_index],
        )

    checksum = 0
    for i, value in enumerate(blocks):
        if value != -1:
            checksum += i * value

    print(checksum)


if __name__ == "__main__":
    main()
