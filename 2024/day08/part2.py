import itertools


def is_valid_antinode(antinode: tuple[int, int], roof: list[str]) -> bool:
    row, col = antinode
    height, width = len(roof), len(roof[0])
    return 0 <= row < height and 0 <= col < width


def main() -> None:
    roof = []
    antennas = {}
    antinodes = set()

    with open("input.txt", "r", encoding="utf-8") as file:
        for row, line in enumerate(file):
            roof.append(line.strip())

            for col, char in enumerate(line.strip()):
                if char == ".":
                    continue

                if char not in antennas:
                    antennas[char] = []

                antennas[char].append((row, col))
                antinodes.add((row, col))

    for positions in antennas.values():
        for pos1, pos2 in itertools.product(positions, positions):
            if pos1 == pos2:
                continue

            dy = pos2[0] - pos1[0]
            dx = pos2[1] - pos1[1]

            factor = 1
            while True:
                antinode = (pos1[0] - factor * dy, pos1[1] - factor * dx)
                if not is_valid_antinode(antinode=antinode, roof=roof):
                    break

                antinodes.add(antinode)
                factor += 1

            factor = 1
            while True:
                antinode = (pos2[0] + factor * dy, pos2[1] + factor * dx)
                if not is_valid_antinode(antinode=antinode, roof=roof):
                    break

                antinodes.add(antinode)
                factor += 1

    print(len(antinodes))


if __name__ == "__main__":
    main()
