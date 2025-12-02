from math import ceil

from fontTools.ttLib import TTFont

from newsflash.svg.box import Box
from newsflash.svg.utils import Point
from newsflash.svg.utils.fonts import lora
from newsflash.svg.element import ElementGroup
from newsflash.svg.elements import build_rectangle_from_bottom_center

from .xy_chart import build_xy_chart


def _build_bars(
    bars: list[float] | list[int],
    chart_box: Box,
) -> ElementGroup:
    elements = ElementGroup()

    for idx, bar in enumerate(bars):
        rect = build_rectangle_from_bottom_center(
            bottom_center=Point(x=idx, y=0.0),
            width=0.9,
            height=bar,
            rounded=0.05,
            classes=["bar"],
            box=chart_box,
        )
        elements.append(rect)

    return elements


def build_barchart(
    values: list[float] | list[int],
    labels: list[str],
    width: float,
    height: float,
    title: str,
    max_y_axis_value: float | None = None,
    font: TTFont = lora,
    title_font_size: int = 32,
    label_font_size: int = 16,
) -> ElementGroup:
    barchart_elements = ElementGroup()

    # TODO: into separate function
    y_step = ceil(max([v / 4 for v in values]))
    max_y_axis_value = y_step * 4

    x_label_positions = list(range(len(labels)))

    x_padding = 0.5

    barchart_elements, chart_box = build_xy_chart(
        labels=labels,
        x_label_positions=x_label_positions,
        width=width,
        height=height,
        title=title,
        min_x_axis_value=0.0,
        max_x_axis_value=len(values) - 1,
        min_y_axis_value=0.0,
        max_y_axis_value=max_y_axis_value,
        x_padding=x_padding,
        font=font,
        title_font_size=title_font_size,
        label_font_size=label_font_size,
    )

    bars = _build_bars(bars=values, chart_box=chart_box)
    barchart_elements.extend(bars)

    return barchart_elements
