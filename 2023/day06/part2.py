import sys
from math import ceil, floor, sqrt
from typing import NamedTuple


class Race(NamedTuple):
    time: int
    distance: int

    def ways_to_win(self) -> int:
        delta = self.time**2 - 4 * self.distance
        hold_min = (-self.time + sqrt(delta)) / -2
        hold_max = (-self.time - sqrt(delta)) / -2
        print(hold_min, hold_max, file=sys.stderr)

        if hold_min == ceil(hold_min):
            hold_min = ceil(hold_min + 1)
        else:
            hold_min = ceil(hold_min)

        if hold_max == floor(hold_max):
            hold_max = floor(hold_max - 1)
        else:
            hold_max = floor(hold_max)

        print(hold_min, hold_max, file=sys.stderr)
        return abs(hold_max - hold_min) + 1


def parse_race(lines: list[str]) -> Race:
    time = lines[0].split(":")[1].strip().replace(" ", "")
    distance = lines[1].split(":")[1].strip().replace(" ", "")
    return Race(time=int(time), distance=int(distance))


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        race = parse_race(lines=file.readlines())
        print(race, file=sys.stderr)
        ways_to_win = race.ways_to_win()

    print(ways_to_win)


if __name__ == "__main__":
    main()
