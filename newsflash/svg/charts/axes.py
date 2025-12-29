from math import ceil, log10, floor
from collections import Counter

from pydantic import BaseModel

from .utils import get_y_label_positions, order_of_magnitude


def smart_round(numbers: list[float]) -> tuple[list[float], int]:
    differences = [numbers[i + 1] - numbers[i] for i in range(len(numbers) - 1)]
    min_difference = min(differences)

    decimal_places = max(0, ceil(-log10(min_difference)))
    return [round(num, decimal_places) for num in numbers], decimal_places


class AxisConfig(BaseModel):
    label_positions: list[float] | list[int]
    label_values: list[str] | list[int] | list[float]
    decimal_places: int
    min_value: float | int
    max_value: float | int
    multiplier: float = 1

    @property
    def labels_as_str(self) -> list[str]:
        if all(isinstance(label, str) for label in self.label_values):
            return self.label_values  # type: ignore
        else:
            return [f"{num:,.{self.decimal_places}f}" for num in self.label_values]


class AxesConfig(BaseModel):
    x: AxisConfig
    y: AxisConfig


def build_y_axis_config(
    values: list[int] | list[float],
    num_labels: int = 5,
    min_value: float | int | None = None,
) -> AxisConfig:
    label_positions = get_y_label_positions(
        values, divide_by=(num_labels - 1), min_y=min_value
    )

    ooms = [order_of_magnitude(l) for l in label_positions]
    multipliers = [pow(10, floor(oom / 3) * 3) for oom in ooms]
    multiplier = Counter(multipliers).most_common(1)[0][0]

    if multiplier != 1:
        label_position_values = [pos / multiplier for pos in label_positions]
    else:
        label_position_values = label_positions
    
    if all([isinstance(x, float) for x in label_position_values]):
        _, decimal_places = smart_round(label_position_values)  # type: ignore
    else:
        decimal_places = 0

    return AxisConfig(
        label_positions=label_positions,
        label_values=label_position_values,
        decimal_places=decimal_places,
        min_value=min_value if min_value is not None else min(label_positions),
        max_value=max(label_positions),
        multiplier=multiplier,
    )


def build_x_axis_config(
    values: list[int] | list[float], num_labels: int = 8
) -> AxisConfig:
    x_step = ceil(len(values) / num_labels)
    label_positions = values[::x_step]

    if all([isinstance(x, float) for x in values]):
        label_positions, decimal_places = smart_round(label_positions)  # type: ignore
    else:
        decimal_places = 0

    min_value = min(values)
    max_value = max(values)

    return AxisConfig(
        label_positions=label_positions,
        label_values=label_positions,
        decimal_places=decimal_places,
        min_value=min_value,
        max_value=max_value,
    )


def build_x_axis_config_barchart(labels: list[str]):
    label_positions = list(range(len(labels)))

    return AxisConfig(
        label_positions=label_positions,
        label_values=labels,
        decimal_places=0,
        min_value=0,
        max_value=len(labels) - 1,
    )
