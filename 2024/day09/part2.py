def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        disk_map = list(map(int, file.read().strip()))

    blocks = []
    for i, value in enumerate(disk_map):
        blocks.extend([i // 2 if i % 2 == 0 else -1] * value)

    for file_id in range(max(blocks), 0, -1):
        first_index = blocks.index(file_id)
        last_index = len(blocks) - 1 - blocks[::-1].index(file_id)
        length = last_index - first_index + 1

        i = 0
        gap_length = 0

        while i < first_index:
            if blocks[i] == -1:
                gap_length += 1

                if gap_length >= length:
                    break

            else:
                gap_length = 0

            i += 1

        if gap_length >= length:
            for j in range(length):
                blocks[i - gap_length + 1 + j], blocks[first_index + j] = (
                    blocks[first_index + j],
                    blocks[i - gap_length + 1 + j],
                )

    checksum = 0
    for i, value in enumerate(blocks):
        if value != -1:
            checksum += i * value

    print(checksum)


if __name__ == "__main__":
    main()
