from shapely import Polygon
from tqdm import trange


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        tiles = [list(map(int, line.strip().split(","))) for line in file]

    polygon = Polygon(tiles)
    area = 0

    for i in trange(len(tiles) - 1):
        for j in range(i + 1, len(tiles)):
            x_min = min(tiles[i][0], tiles[j][0])
            y_min = min(tiles[i][1], tiles[j][1])
            x_max = max(tiles[i][0], tiles[j][0])
            y_max = max(tiles[i][1], tiles[j][1])

            rectangle = Polygon(
                [
                    (x_min, y_min),
                    (x_max, y_min),
                    (x_max, y_max),
                    (x_min, y_max),
                ]
            )

            if polygon.contains(rectangle):
                area = max(area, (x_max - x_min + 1) * (y_max - y_min + 1))

    print(area)


if __name__ == "__main__":
    main()
