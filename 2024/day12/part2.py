from shapely import LineString, MultiLineString, Polygon
from shapely.ops import unary_union


def is_collinear(
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
) -> bool:
    det = (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1])
    return abs(det) == 0


def number_of_sides(boundary: LineString | MultiLineString) -> int:
    if isinstance(boundary, MultiLineString):
        return sum(number_of_sides(g) for g in boundary.geoms)

    coords = boundary.coords[:-1]
    return sum(
        not is_collinear(coords[i - 2], coords[i - 1], coords[i])
        for i in range(len(coords))
    )


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        garden = [line.strip() for line in file]

    height, width = len(garden), len(garden[0])

    def flood_fill(
        pos: tuple[int, int],
        region: set[tuple[int, int]],
    ) -> None:
        region.add(pos)

        for dy, dx in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            neighbor = (pos[0] + dx, pos[1] + dy)
            if (
                0 <= neighbor[0] < width
                and 0 <= neighbor[1] < height
                and neighbor not in region
                and garden[neighbor[1]][neighbor[0]] == garden[pos[1]][pos[0]]
            ):
                flood_fill(pos=neighbor, region=region)

    regions = []
    visited = set()
    for x in range(width):
        for y in range(height):
            pos = (x, y)
            if pos in visited:
                continue

            region = set()
            flood_fill(pos=pos, region=region)
            regions.append(region)
            visited.update(region)

    polygons = [
        unary_union(
            [
                Polygon(
                    [
                        (pos[0], pos[1]),
                        (pos[0] + 1, pos[1]),
                        (pos[0] + 1, pos[1] + 1),
                        (pos[0], pos[1] + 1),
                    ]
                )
                for pos in region
            ]
        )
        for region in regions
    ]

    print(
        sum(
            int(polygon.area * number_of_sides(polygon.boundary))
            for polygon in polygons
        )
    )


if __name__ == "__main__":
    main()
