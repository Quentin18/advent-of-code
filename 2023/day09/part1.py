import sys

import numpy as np


def predict(history: np.ndarray) -> int:
    sequence = history.copy()
    sequences = []
    while not (sequence == 0).all():
        sequences.append(sequence)
        sequence = np.diff(sequence)

    print(sequences, file=sys.stderr)

    prediction = 0
    for sequence in sequences[::-1]:
        prediction = sequence[-1] + prediction

    print(prediction, file=sys.stderr)
    return prediction


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        predictions_sum = 0
        for line in file:
            history = np.array([int(i) for i in line.strip().split()])
            predictions_sum += predict(history=history)

    print(predictions_sum)


if __name__ == "__main__":
    main()
