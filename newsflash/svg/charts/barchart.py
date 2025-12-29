from fontTools.ttLib import TTFont

from newsflash.svg.box import Box
from newsflash.svg.utils import Point
from newsflash.svg.utils.fonts import lora
from newsflash.svg.element import ElementGroup
from newsflash.svg.elements import build_rectangle_from_bottom_center

from .xy_chart import build_xy_chart
from .axes import (
    AxesConfig,
    build_y_axis_config,
    build_x_axis_config_barchart,
)


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
    font: TTFont = lora,
    title_font_size: int = 32,
    label_font_size: int = 16,
) -> ElementGroup:
    barchart_elements = ElementGroup()

    x_padding = 0.5
    axes = AxesConfig(
        x=build_x_axis_config_barchart(labels=labels),
        y=build_y_axis_config(values=values, min_value=0),
    )

    barchart_elements, chart_box = build_xy_chart(
        axes=axes,
        width=width,
        height=height,
        title=title,
        x_padding=x_padding,
        font=font,
        title_font_size=title_font_size,
        label_font_size=label_font_size,
    )

    bars = _build_bars(bars=values, chart_box=chart_box)
    barchart_elements.extend(bars)

    return barchart_elements
