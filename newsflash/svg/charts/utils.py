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
    recursive_call: bool = True,
) -> list[float] | list[int]:
    min_y_to_use = min(values) if min_y is None else min_y
    max_y_to_use = max(values) if max_y is None else max_y

    step = nice_ceil((max_y_to_use - min_y_to_use) / divide_by)

    min_y_rounded = floor(min_y_to_use / step) * step
    max_y_rounded = ceil(max_y_to_use / step) * step

    y_label_positions = []
    current_label = min_y_rounded
    while current_label <= max_y_rounded:
        y_label_positions.append(current_label)
        current_label += step

    if recursive_call and len(y_label_positions) > (divide_by + 1):
        return get_y_label_positions(
            values=values,
            min_y=min_y,
            max_y=max_y,
            divide_by=divide_by - 1,
            recursive_call=False,
        )

    return y_label_positions


def nice_ceil(x: float) -> float:
    oom = order_of_magnitude(x)
    factor = pow(10, oom)
    return ceil(x / factor) * factor
