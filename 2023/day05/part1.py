from __future__ import annotations


class Range:
    def __init__(
        self,
        destination_start: int,
        source_start: int,
        length: int,
    ) -> None:
        self.destination_start = destination_start
        self.source_start = source_start
        self.length = length

        self.destination_end = destination_start + length - 1
        self.source_end = source_start + length - 1
        self.delta = self.destination_start - self.source_start

    @staticmethod
    def parse(line: str) -> Range:
        destination_start, source_start, length = line.strip().split()
        return Range(
            destination_start=int(destination_start),
            source_start=int(source_start),
            length=int(length),
        )

    def __contains__(self, item: int) -> bool:
        return self.source_start <= item <= self.source_end

    def get_destination(self, source: int) -> int:
        return source + self.delta


class Converter:
    def __init__(self, ranges: list[Range]) -> None:
        self.ranges = ranges

    @staticmethod
    def parse(lines: list[str]) -> list[Converter]:
        ranges = []
        converters = []

        for line in lines:
            if "map" in line:
                continue

            if not line.strip():
                converters.append(Converter(ranges=ranges))
                ranges = []
            else:
                ranges.append(Range.parse(line=line))

        converters.append(Converter(ranges=ranges))

        return converters

    def convert(self, source: int) -> int:
        for r in self.ranges:
            if source in r:
                return r.get_destination(source=source)

        return source


def parse_seeds(line: str) -> list[int]:
    return [int(i) for i in line.split(":")[1].strip().split()]


def get_lowest_location(lines: list[str]) -> int:
    seeds = parse_seeds(line=lines[0])
    converters = Converter.parse(lines=lines[2:])

    locations = []

    for seed in seeds:
        for converter in converters:
            seed = converter.convert(source=seed)
        locations.append(seed)

    return min(locations)


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        response = get_lowest_location(lines=file.readlines())

    print(response)


if __name__ == "__main__":
    main()
