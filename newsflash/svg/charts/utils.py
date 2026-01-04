from math import floor, log10
from decimal import Decimal
from bisect import bisect_left


def order_of_magnitude(value: float) -> int:
    """Returns the order of magnitude of a given value."""
    if value == 0:
        return 0

    return floor(log10(abs(value)))


def n_significant_figures(value: float) -> int:
    """Returns the number of significant figures in a given float value."""
    d = Decimal(str(value)).quantize(Decimal("0.0000000001")).normalize()
    digits = d.as_tuple().digits
    return len(digits)


def order_of_magnitude_for_significant_figures(value: float) -> int:
    n_sig_figs = n_significant_figures(value)
    oom = order_of_magnitude(value)
    return oom - (n_sig_figs - 1)


STEP_CANDIDATES = [0.25, 0.5, 1, 2, 2.5, 5, 10]


def get_y_label_positions(
    values: list[float] | list[int],
    min_y: float | int | None = None,
    max_y: float | int | None = None,
    divide_by: int = 4,
) -> list[float] | list[int]:
    min_y_to_use = min(values) if min_y is None else min_y
    max_y_to_use = max(values) if max_y is None else max_y

    step = 0
    highest_score = 0.0
    num_steps = 0

    for divide_by in [4, 3, 5]:
        ideal_step = (max_y_to_use - min_y_to_use) / divide_by
        normalized_ideal_step = ideal_step / pow(10, order_of_magnitude(ideal_step))

        idx = bisect_left(STEP_CANDIDATES, normalized_ideal_step)
        next_step = STEP_CANDIDATES[idx]

        score = normalized_ideal_step / next_step
        if score > highest_score:
            highest_score = score
            step = next_step * pow(10, order_of_magnitude(ideal_step))
            num_steps = divide_by

    y_label_positions = []
    current_label = min_y_to_use
    for _ in range(num_steps + 1):
        y_label_positions.append(current_label)
        current_label += step

    return y_label_positions
