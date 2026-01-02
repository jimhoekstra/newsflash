import pytest

from newsflash.svg.charts.utils import order_of_magnitude


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
