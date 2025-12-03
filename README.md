# 🎄 Advent of Code 🎄

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://pre-commit.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](https://github.com/Quentin18/advent-of-code)
[![CI](https://github.com/Quentin18/advent-of-code/actions/workflows/build.yml/badge.svg)](https://github.com/Quentin18/advent-of-code/actions/workflows/build.yml)

This repository contains my Python solutions to the [Advent of Code](https://adventofcode.com/) puzzles.

## Installation

Clone the repository:

```bash
git clone https://github.com/Quentin18/advent-of-code.git
```

Move to the root of the repository:

```bash
cd advent-of-code/
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file with your session cookie:

```bash
echo -e "SESSION_COOKIE=your_session_cookie" > .env
```

## Usage

- The repository contains **one folder per year**.
- For each year, there is **one folder per day** named `day[xx]`.
- For each day, the following files are present:
    - Test input in `input_test.txt`
    - Puzzle input in `input.txt`
    - Script to solve part 1 in `part1.py`
    - Script to solve part 2 in `part2.py`

### Run a solution

Move in the directory of the puzzle day (example with day 1 of 2023):

```bash
cd 2023/day01/
```

Run the `part1.py` script to get the solution of the first part:

```bash
python part1.py
```

Run the `part2.py` script to get the solution of the second part:

```bash
python part2.py
```

### Make a new day

To make the folder for a new day, use the `main` script (example with day 1 of 2023):

```bash
python main.py -y 2023 -d 1
```

## Author

[Quentin Deschamps](mailto:quentindeschamps18@gmail.com)

## License

[MIT](https://choosealicense.com/licenses/mit/)
