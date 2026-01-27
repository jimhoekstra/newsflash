import pytest

from newsflash.svg.charts.utils import (
    order_of_magnitude,
    n_significant_figures,
    order_of_magnitude_for_significant_figures,
    smart_round,
    get_step_decimal_places,
)


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, 0),
        (5, 0),
        (75, 1),
        (500.2, 2),
        (0.5111, -1),
        (0.023, -2),
        (-7800, 3),
    ],
)
def test_order_of_magnitude(value: int, expected: int) -> None:
    assert order_of_magnitude(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0.25, 2),
        (2, 1),
        (200, 1),
        (0.00456, 3),
        (12345.6789, 9),
    ],
)
def test_n_significant_figures(value: float, expected: int) -> None:
    assert n_significant_figures(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0.25, -2),
        (2, 0),
        (200, 2),
        (0.00456, -5),
        (12345.6789, -4),
    ],
)
def test_order_of_magnitude_for_significant_figures(
    value: float, expected: int
) -> None:
    assert order_of_magnitude_for_significant_figures(value) == expected


@pytest.mark.parametrize(
    "numbers, expected_rounded, expected_decimal_places",
    [
        (
            [0.0, 0.25, 0.5, 0.75, 1.0],
            [0.0, 0.2, 0.5, 0.8, 1.0],
            1,
        ),
        (
            [0, 0.1, 1.01, 2.2, 3, 4],
            [0, 0.1, 1, 2.2, 3, 4],
            1,
        ),
    ],
)
def test_smart_round(
    numbers: list[float],
    expected_rounded: list[float],
    expected_decimal_places: int,
) -> None:
    rounded, decimal_places = smart_round(numbers)
    assert rounded == expected_rounded
    assert decimal_places == expected_decimal_places


@pytest.mark.parametrize(
    "numbers, expected_decimal_places",
    [
        (
            [0.0, 0.25, 0.5, 0.75, 1.0],
            2,  # because 0.25 requires 2 decimal places
        ),
        (
            [0, 0.1, 1.01, 2.2, 3, 4],
            1,  # because 0.1 requires 1 decimal place
        ),
    ],
)
def test_get_step_decimal_places(
    numbers: list[float],
    expected_decimal_places: int,
) -> None:
    decimal_places = get_step_decimal_places(numbers)
    assert decimal_places == expected_decimal_places
