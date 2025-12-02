from .part1 import is_valid


def test_is_valid_when_true():
    conditions = "#.#.###"
    sizes = [1, 1, 3]
    actual = is_valid(conditions=conditions, sizes=sizes)
    assert actual is True


def test_is_valid_when_false():
    conditions = "##..###"
    sizes = [1, 1, 3]
    actual = is_valid(conditions=conditions, sizes=sizes)
    assert actual is False
