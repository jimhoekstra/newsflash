from math import floor, log10, ceil


def order_of_magnitude(value: float) -> int:
    """Returns the order of magnitude of a given value."""
    if value == 0:
        return 0

    return floor(log10(abs(value)))


def get_y_label_positions(
    values: list[float] | list[int],
    min_y: float | int | None = None,
    max_y: float | int | None = None,
    divide_by: int = 4,
) -> list[float] | list[int]:
    min_y_to_use = min(values) if min_y is None else min_y
    max_y_to_use = max(values) if max_y is None else max_y

    min_y_to_use = nice_round(min_y_to_use, reference=max_y_to_use)
    max_y_to_use = nice_round(max_y_to_use, reference=max_y_to_use)

    step = (max_y_to_use - min_y_to_use) / divide_by

    y_label_positions = []
    current_label = min_y_to_use
    while current_label <= max_y_to_use:
        y_label_positions.append(current_label)
        current_label += step

    return y_label_positions


def nice_ceil(x: float) -> float:
    oom = order_of_magnitude(x)
    factor = pow(10, oom)
    return ceil(x / factor) * factor


def nice_round(x: float, reference: float) -> float:
    oom = order_of_magnitude(reference)
    factor = pow(10, oom)
    return round(x / factor) * factor
