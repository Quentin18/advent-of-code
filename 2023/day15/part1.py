import sys


def calculate_hash(s: str) -> int:
    h = 0
    for c in s:
        h = ((h + ord(c)) * 17) % 256
    return h


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        sequence = file.read().strip().split(",")

    print(sequence, file=sys.stderr)
    hash_values = [calculate_hash(s=s) for s in sequence]
    print(hash_values, file=sys.stderr)
    print(sum(hash_values))


if __name__ == "__main__":
    main()
