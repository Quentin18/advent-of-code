# 🎄 Advent of Code 🎄

[![CI](https://github.com/Quentin18/advent-of-code/actions/workflows/build.yml/badge.svg)](https://github.com/Quentin18/advent-of-code/actions/workflows/build.yml)
[![codestyle](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](https://github.com/Quentin18/advent-of-code)

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

To make the folder for a new day, use the `make_new_day.sh` script (example with day 1 of 2023):

```bash
./make_new_day.sh 2023/day01
```

## Author

[Quentin Deschamps](mailto:quentindeschamps18@gmail.com)

## License

[MIT](https://choosealicense.com/licenses/mit/)
