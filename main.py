import argparse
import os
import shutil
from contextlib import closing
from pathlib import Path

from dotenv import load_dotenv

from aoc_client import AdventOfCodeClient


def main() -> None:
    parser = argparse.ArgumentParser(description="Advent of Code CLI")
    subparsers = parser.add_subparsers(dest="command")

    parser_make = subparsers.add_parser("make")
    parser_make.add_argument("--year", "-y", type=int, required=True)
    parser_make.add_argument("--day", "-d", type=int, required=True)

    args = parser.parse_args()

    load_dotenv()
    session_cookie = os.environ["SESSION_COOKIE"]

    with closing(AdventOfCodeClient(session_cookie=session_cookie)) as aoc_client:
        puzzle_input = aoc_client.get_puzzle_input(
            year=args.year,
            day=args.day,
        )
        puzzle_test_inputs = aoc_client.get_puzzle_test_inputs(
            year=args.year,
            day=args.day,
        )

    puzzle_dir = Path(f"{args.year}/day{args.day:02}")
    puzzle_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile("template.py", puzzle_dir / "part1.py")

    with open(puzzle_dir / "input.txt", "w", encoding="utf-8") as file:
        file.write(puzzle_input)

    for i, test_input in enumerate(puzzle_test_inputs):
        suffix = f"_{i + 1}" if i > 0 else ""
        with open(
            puzzle_dir / f"input_test{suffix}.txt",
            "w",
            encoding="utf-8",
        ) as file:
            file.write(test_input)


if __name__ == "__main__":
    main()
