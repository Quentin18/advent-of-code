def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        available_patterns = set(next(file).strip().split(", "))
        next(file)
        designs = [line.strip() for line in file]

    def is_design_possible(design: str) -> bool:
        if design in available_patterns:
            return True

        for pattern in available_patterns:
            if design.startswith(pattern) and is_design_possible(
                design[len(pattern) :]
            ):
                return True

        return False

    print(sum(is_design_possible(design) for design in designs))


if __name__ == "__main__":
    main()
