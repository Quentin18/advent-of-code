import sys


def calculate_hash(s: str) -> int:
    h = 0
    for c in s:
        h = ((h + ord(c)) * 17) % 256
    return h


def get_boxes(sequence: list[str]) -> dict[int, list[tuple[str, int]]]:
    boxes = {}

    for s in sequence:
        if s[-1] == "-":
            label = s.split("-")[0]
            box = calculate_hash(s=label)
            if box not in boxes:
                continue

            for lens in boxes[box]:
                if lens[0] == label:
                    boxes[box].remove(lens)
                    break
        else:
            label, focal_length = s.split("=")
            focal_length = int(focal_length)
            box = calculate_hash(s=label)
            if box not in boxes:
                boxes[box] = [(label, focal_length)]
                continue

            replaced = False
            for i, lens in enumerate(boxes[box]):
                if lens[0] == label:
                    boxes[box][i] = (label, focal_length)
                    replaced = True
                    break

            if not replaced:
                boxes[box].append((label, focal_length))

    return boxes


def calculate_focusing_power(boxes: dict[int, list[tuple[str, int]]]) -> int:
    power = 0

    for box in boxes:
        for slot, lens in enumerate(boxes[box]):
            power += (box + 1) * (slot + 1) * lens[1]

    return power


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        sequence = file.read().strip().split(",")

    print(sequence, file=sys.stderr)
    boxes = get_boxes(sequence=sequence)
    print(boxes, file=sys.stderr)
    power = calculate_focusing_power(boxes=boxes)
    print(power)


if __name__ == "__main__":
    main()
