def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        grid = [line.strip() for line in file]

    beams = {grid[0].index("S"): 1}

    for line in grid[1:]:
        next_beams = {}
        for beam, count in beams.items():
            if line[beam] == "^":
                if beam > 0:
                    if beam - 1 not in next_beams:
                        next_beams[beam - 1] = count
                    else:
                        next_beams[beam - 1] += count

                if beam < len(line) - 1:
                    if beam + 1 not in next_beams:
                        next_beams[beam + 1] = count
                    else:
                        next_beams[beam + 1] += count
            elif beam not in next_beams:
                next_beams[beam] = count
            else:
                next_beams[beam] += count

        beams = next_beams

    print(sum(beams.values()))


if __name__ == "__main__":
    main()
