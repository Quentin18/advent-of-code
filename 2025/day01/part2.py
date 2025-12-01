def main() -> None:
    dial = 50
    password = 0

    with open("input.txt", "r", encoding="utf-8") as file:
        for rotation in file:
            rotation = rotation.strip()
            direction = rotation[0]
            distance = int(rotation[1:])

            if direction == "R":
                password += (dial + distance) // 100
                dial = (dial + distance) % 100
            elif direction == "L":
                if distance == dial and dial != 0:
                    password += 1
                elif distance > dial:
                    password += (distance - dial) // 100
                    if dial != 0:
                        password += 1
                dial = (dial - distance) % 100
            else:
                raise ValueError(f"Invalid direction: {direction}")

    print(password)


if __name__ == "__main__":
    main()
