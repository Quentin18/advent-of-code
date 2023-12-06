from part2 import SourceRange, DestinationSourceRange


def test_get_destination():
    # Given
    source_range = SourceRange(start=79, length=14)
    destination_source_range = DestinationSourceRange(
        destination_start=52,
        source_start=50,
        length=48,
    )

    # When
    actual = destination_source_range.get_destination(source_range=source_range)

    # Then
    assert actual.start == 81
    assert actual.end == 94


def test_get_destination_overlap():
    # Given
    source_range = SourceRange(start=90, length=9)
    destination_source_range_1 = DestinationSourceRange(
        destination_start=60,
        source_start=56,
        length=37,
    )
    destination_source_range_2 = DestinationSourceRange(
        destination_start=56,
        source_start=93,
        length=4,
    )

    # When
    actual_1 = destination_source_range_1.get_destination(source_range=source_range)
    actual_2 = destination_source_range_2.get_destination(source_range=source_range)

    # Then
    assert actual_1.start == 94
    assert actual_1.end == 96
    assert actual_2.start == 56
    assert actual_2.end == 59
