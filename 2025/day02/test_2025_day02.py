import pytest

from .part2 import is_valid_id


@pytest.mark.parametrize(
    "id_,expected",
    [
        (12341234, False),
        (123123123, False),
        (1212121212, False),
        (1111111, False),
        (123456789, True),
    ],
)
def test_is_valid_id(id_: int, expected: bool):
    assert is_valid_id(id_) == expected
