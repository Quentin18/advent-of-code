from __future__ import annotations

import sys


class SourceRange:
    def __init__(self, start: int, length: int) -> None:
        self.start = start
        self.length = length
        self.end = start + length - 1

    @staticmethod
    def parse(line: str) -> list[SourceRange]:
        numbers = [int(i) for i in line.split(":")[1].strip().split()]

        ranges = []
        for i in range(0, len(numbers), 2):
            ranges.append(SourceRange(start=numbers[i], length=numbers[i + 1]))

        ranges.sort(key=lambda r: r.start)

        return ranges

    def __repr__(self) -> str:
        return f"SourceRange(start={self.start}, end={self.end}, length={self.length})"

    __str__ = __repr__


class DestinationSourceRange:
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
    def parse(line: str) -> DestinationSourceRange:
        destination_start, source_start, length = line.strip().split()
        return DestinationSourceRange(
            destination_start=int(destination_start),
            source_start=int(source_start),
            length=int(length),
        )

    def __contains__(self, item: SourceRange) -> bool:
        # return true when overlapping
        return (
            self.source_start <= item.start <= self.source_end
            or self.source_start <= item.end <= self.source_end
            or item.start <= self.source_start <= item.end
            or item.start <= self.source_end <= item.end
        )

    def get_destination(self, source_range: SourceRange) -> SourceRange:
        source_min = max(source_range.start, self.source_start)
        source_max = min(source_range.end, self.source_end)
        return SourceRange(
            start=source_min + self.delta,
            length=source_max - source_min + 1,
        )

    def __repr__(self) -> str:
        return (
            f"DestinationSourceRange("
            f"source=[{self.source_start}, {self.source_end}]), "
            f"destination=[{self.destination_start}, {self.destination_end}], "
            f"length={self.length})"
        )

    __str__ = __repr__


class Converter:
    def __init__(self, ranges: list[DestinationSourceRange]) -> None:
        self.ranges = ranges

    @staticmethod
    def clean_ranges(ranges: list[DestinationSourceRange]) -> None:
        ranges.sort(key=lambda r: r.source_start)

        # add identity ranges between given ranges
        additional_ranges = []
        for i in range(len(ranges) - 1):
            if ranges[i].source_end != ranges[i + 1].source_start - 1:
                source_start = ranges[i].source_end + 1
                source_end = ranges[i + 1].source_start - 1
                additional_ranges.append(
                    DestinationSourceRange(
                        destination_start=source_start,
                        source_start=source_start,
                        length=source_end - source_start + 1,
                    )
                )

        if additional_ranges:
            print("add additional ranges:", additional_ranges, file=sys.stderr)

        ranges.extend(additional_ranges)
        ranges.sort(key=lambda r: r.source_start)

        # check ranges
        for i in range(len(ranges) - 1):
            assert ranges[i].source_end == ranges[i + 1].source_start - 1, (
                "wrong ranges"
            )

    @staticmethod
    def parse(lines: list[str]) -> list[Converter]:
        ranges = []
        converters = []

        for line in lines:
            if "map" in line:
                continue

            if not line.strip():
                Converter.clean_ranges(ranges=ranges)
                converters.append(Converter(ranges=ranges))
                ranges = []
            else:
                ranges.append(DestinationSourceRange.parse(line=line))

        converters.append(Converter(ranges=ranges))

        return converters

    def get_destination_ranges(
        self,
        source_ranges: list[SourceRange],
    ) -> list[SourceRange]:
        destination_ranges = []

        min_ranges_source = min(r.source_start for r in self.ranges)
        max_ranges_source = max(r.source_end for r in self.ranges)

        for source_range in source_ranges:
            destination_length = 0

            for destination_source_range in self.ranges:
                if source_range in destination_source_range:
                    destination_ranges.append(
                        destination_source_range.get_destination(
                            source_range=source_range,
                        )
                    )
                    destination_length += destination_ranges[-1].length

            # before or after all ranges
            if (
                source_range.end < min_ranges_source
                or source_range.start > max_ranges_source
            ):
                destination_ranges.append(
                    SourceRange(
                        start=source_range.start,
                        length=source_range.length,
                    )
                )
                destination_length += destination_ranges[-1].length

            # a part of the range if before all ranges
            if source_range.start <= min_ranges_source <= source_range.end:
                destination_ranges.append(
                    SourceRange(
                        start=source_range.start,
                        length=min_ranges_source - source_range.start,
                    )
                )

                destination_length += destination_ranges[-1].length

            # a part of the range if after all ranges
            if source_range.start <= max_ranges_source < source_range.end:
                destination_ranges.append(
                    SourceRange(
                        start=max_ranges_source + 1,
                        length=source_range.end - max_ranges_source,
                    )
                )
                destination_length += destination_ranges[-1].length

            assert destination_length == source_range.length

        # remove ranges with 0-length (maybe could be avoided)
        destination_ranges = [r for r in destination_ranges if r.length > 0]

        destination_ranges.sort(key=lambda r: r.start)

        # check all lengths
        assert sum(r.length for r in source_ranges) == sum(
            r.length for r in destination_ranges
        )

        return destination_ranges


def get_lowest_location(lines: list[str]) -> int:
    source_ranges = SourceRange.parse(line=lines[0])
    converters = Converter.parse(lines=lines[2:])

    print("seeds:", source_ranges, file=sys.stderr)
    for i, converter in enumerate(converters):
        source_ranges = converter.get_destination_ranges(source_ranges=source_ranges)
        print(f"iteration {i}: {source_ranges}", file=sys.stderr)

    return source_ranges[0].start


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        response = get_lowest_location(lines=file.readlines())

    print(response)


if __name__ == "__main__":
    main()
