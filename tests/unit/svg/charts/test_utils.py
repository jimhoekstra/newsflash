import pytest

from newsflash.svg.charts.utils import order_of_magnitude, nice_ceil


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
    ]
)
def test_order_of_magnitude(value: int, expected: int) -> None:
    assert order_of_magnitude(value) == expected


@pytest.mark.parametrize(
    "x, expected",
    [
        (2, 2),
        (5.3, 6),
        (23, 30),
        (0.76, 0.8),
        (0.034, 0.04),
        (780, 800),
        (0.0023, 0.003),
    ]
)
def test_nice_ceil(x: float, expected: float) -> None:
    assert nice_ceil(x) == expected
