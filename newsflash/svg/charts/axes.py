from math import ceil, log10

from pydantic import BaseModel

from .utils import get_y_label_positions


def smart_round(numbers: list[float]) -> list[str]:
    differences = [numbers[i + 1] - numbers[i] for i in range(len(numbers) - 1)]
    min_difference = min(differences)

    decimal_places = max(0, ceil(-log10(min_difference)) + 1)
    return [f"{num:.{decimal_places}f}" for num in numbers]


class AxisConfig(BaseModel):
    label_positions: list[float] | list[int]
    label_values: list[str] | list[int] | list[float]
    min_value: float | int
    max_value: float | int

    @property
    def labels_as_str(self) -> list[str]:
        if all(isinstance(label, float) for label in self.label_values):
            return smart_round(self.label_values)  # type: ignore
        elif all(isinstance(label, int) for label in self.label_values):
            return [str(label) for label in self.label_values]
        else:
            return self.label_values  # type: ignore


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
    if min_value is None:
        min_value = min(label_positions)
    max_value = max(label_positions)

    return AxisConfig(
        label_positions=label_positions,
        label_values=label_positions,
        min_value=min_value,
        max_value=max_value,
    )


def build_x_axis_config(
    values: list[int] | list[float], num_labels: int = 8
) -> AxisConfig:
    x_step = ceil(len(values) / num_labels)
    label_positions = values[::x_step]

    min_value = min(values)
    max_value = max(values)

    return AxisConfig(
        label_positions=label_positions,
        label_values=label_positions,
        min_value=min_value,
        max_value=max_value,
    )


def build_x_axis_config_barchart(labels: list[str]):
    label_positions = list(range(len(labels)))

    return AxisConfig(
        label_positions=label_positions,
        label_values=labels,
        min_value=0,
        max_value=len(labels) - 1,
    )
