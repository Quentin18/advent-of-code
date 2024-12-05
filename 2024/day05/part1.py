import sys


def main() -> None:
    page_ordering_rules = []
    page_updates = []

    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file:
            if "|" in line:
                page_ordering_rules.append(tuple(map(int, line.strip().split("|"))))
            elif "," in line:
                page_updates.append(list(map(int, line.strip().split(","))))

    middle_page_number_sum = 0

    for page_update in page_updates:
        print(page_update, file=sys.stderr)

        correct = True

        for i, page in enumerate(page_update):
            if not all(
                (page, prev_page) not in page_ordering_rules
                for prev_page in page_update[:i]
            ):
                print(page, "is not correct", file=sys.stderr)
                correct = False
                break

        if correct:
            middle_page_number_sum += page_update[(len(page_update) - 1) // 2]

    print(middle_page_number_sum)


if __name__ == "__main__":
    main()
