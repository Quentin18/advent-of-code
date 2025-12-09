def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        grid = [line.strip() for line in file]

    beams = {grid[0].index("S")}
    splits = 0

    for line in grid[1:]:
        next_beams = set()
        for beam in beams:
            if line[beam] == "^":
                splits += 1
                if beam > 0:
                    next_beams.add(beam - 1)
                if beam < len(line) - 1:
                    next_beams.add(beam + 1)
            else:
                next_beams.add(beam)

        beams = next_beams

    print(splits)


if __name__ == "__main__":
    main()
