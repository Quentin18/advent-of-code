import itertools


def is_valid_antinode(antinode: tuple[int, int], roof: list[str]) -> bool:
    row, col = antinode
    height, width = len(roof), len(roof[0])
    return 0 <= row < height and 0 <= col < width


def main() -> None:
    roof = []
    antennas = {}

    with open("input.txt", "r", encoding="utf-8") as file:
        for row, line in enumerate(file):
            roof.append(line.strip())

            for col, char in enumerate(line.strip()):
                if char == ".":
                    continue

                if char not in antennas:
                    antennas[char] = []

                antennas[char].append((row, col))

    antinodes = set()

    for positions in antennas.values():
        for pos1, pos2 in itertools.product(positions, positions):
            if pos1 == pos2:
                continue

            dy = pos2[0] - pos1[0]
            dx = pos2[1] - pos1[1]

            for antinode in (
                (pos1[0] - dy, pos1[1] - dx),
                (pos2[0] + dy, pos2[1] + dx),
            ):
                if is_valid_antinode(antinode=antinode, roof=roof):
                    antinodes.add(antinode)

    print(len(antinodes))


if __name__ == "__main__":
    main()
