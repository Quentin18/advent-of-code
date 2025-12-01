def main() -> None:
    dial = 50
    password = 0

    with open("input.txt", "r", encoding="utf-8") as file:
        for rotation in file:
            rotation = rotation.strip()
            direction = rotation[0]
            distance = int(rotation[1:])

            if direction == "R":
                dial = (dial + distance) % 100
            elif direction == "L":
                dial = (dial - distance) % 100
            else:
                raise ValueError(f"Invalid direction: {direction}")

            if dial == 0:
                password += 1

    print(password)


if __name__ == "__main__":
    main()
