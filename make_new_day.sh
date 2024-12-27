#!/bin/bash

set -eo pipefail

if test -z "$1"; then
  echo >&2 "usage: ./make_new_day 2023/day01"
  exit 1
fi

echo "make day $1"

mkdir -p "$1"
cp template.py "$1"/part1.py
touch "$1"/input_test.txt
git add "$1"
