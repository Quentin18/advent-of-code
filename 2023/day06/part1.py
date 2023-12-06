import sys
from math import ceil, floor, prod, sqrt
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


def parse_races(lines: list[str]) -> list[Race]:
    times = lines[0].split(":")[1].strip().split()
    distances = lines[1].split(":")[1].strip().split()
    return [Race(time=int(t), distance=int(d)) for t, d in zip(times, distances)]


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        races = parse_races(lines=file.readlines())
        ways_to_win = [race.ways_to_win() for race in races]
        print(ways_to_win, file=sys.stderr)
        response = prod(ways_to_win)

    print(response)


if __name__ == "__main__":
    main()
