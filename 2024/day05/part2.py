import sys


def main() -> None:
    page_ordering_rules = []
    page_updates = []

    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file:
            if "|" in line:
                prev_page, next_page = list(map(int, line.strip().split("|")))
                page_ordering_rules.append((prev_page, next_page))
            elif "," in line:
                page_updates.append(list(map(int, line.strip().split(","))))

    middle_page_number_sum = 0

    for page_update in page_updates:
        print(f"{page_update=}", file=sys.stderr)

        corrected_page_update = page_update.copy()

        i = 0
        while i < len(corrected_page_update):
            updated = False

            for j, prev_page in enumerate(corrected_page_update[:i]):
                if (corrected_page_update[i], prev_page) in page_ordering_rules:
                    print(
                        f"swap {corrected_page_update[i]} and {corrected_page_update[j]}",
                        file=sys.stderr,
                    )
                    corrected_page_update[i], corrected_page_update[j] = (
                        corrected_page_update[j],
                        corrected_page_update[i],
                    )
                    i = j
                    updated = True
                    break

            if not updated:
                i += 1

        if page_update != corrected_page_update:
            print(f"{corrected_page_update=}", file=sys.stderr)
            middle_page_number_sum += corrected_page_update[
                (len(corrected_page_update) - 1) // 2
            ]

    print(middle_page_number_sum)


if __name__ == "__main__":
    main()
