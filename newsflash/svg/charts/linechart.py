from math import ceil, floor

from fontTools.ttLib import TTFont

from newsflash.svg.box import Box
from newsflash.svg.utils import Point
from newsflash.svg.utils.fonts import lora
from newsflash.svg.element import ElementGroup
from newsflash.svg.elements import build_path

from .xy_chart import build_xy_chart


def _build_line(
    xs: list[float] | list[int],
    ys: list[float] | list[int],
    chart_box: Box,
) -> ElementGroup:
    elements = ElementGroup()

    line_points = [
        Point(
            x=x,
            y=y,
        )
        for x, y in list(zip(xs, ys))
    ]

    path = build_path(
        points=line_points,
        box=chart_box,
        classes=["line-path"],
    )

    elements.append(path)
    return elements


def build_linechart(
    xs: list[float] | list[int],
    ys: list[float] | list[int],
    width: float,
    height: float,
    title: str,
    font: TTFont = lora,
    title_font_size: int = 32,
    label_font_size: int = 16,
) -> ElementGroup:
    linechart_elements = ElementGroup()

    # TODO: into separate function
    y_step = ceil((max(ys) - min(ys)) / 3)
    min_y_axis_value = floor(min(ys) / y_step) * y_step
    max_y_axis_value = ceil(max(ys) / y_step) * y_step
    num_y_labels = round((max_y_axis_value - min_y_axis_value) / y_step) + 1
    y_label_positions = [min_y_axis_value + y_step * i for i in range(num_y_labels)]

    x_step = ceil((max(xs) - min(xs)) / 8)
    x_label_positions = xs[::x_step]
    x_labels = [str(x) for x in x_label_positions]

    x_padding = len(xs) / 50
    min_x_axis_value = min(xs)
    max_x_axis_value = max(xs)

    linechart_elements, chart_box = build_xy_chart(
        labels=x_labels,
        x_label_positions=x_label_positions,
        y_label_positions=y_label_positions,
        width=width,
        height=height,
        title=title,
        min_x_axis_value=min_x_axis_value,
        max_x_axis_value=max_x_axis_value,
        min_y_axis_value=min_y_axis_value,
        max_y_axis_value=max_y_axis_value,
        x_padding=x_padding,
        font=font,
        title_font_size=title_font_size,
        label_font_size=label_font_size,
    )

    line = _build_line(xs=xs, ys=ys, chart_box=chart_box)
    linechart_elements.extend(line)

    return linechart_elements
