from fontTools.ttLib import TTFont

from newsflash.svg.box import Box
from newsflash.svg.utils import Point
from newsflash.svg.utils.fonts import lora
from newsflash.svg.element import ElementGroup
from newsflash.svg.elements import (
    build_rectangle_from_bottom_center,
    build_rectangle_from_top_center,
)

from .xy_chart import build_xy_chart
from .axes import (
    AxesConfig,
    build_x_axis_config_barchart,
    build_y_axis_config_from_step,
)


def build_bars(
    bars: list[float] | list[int],
    chart_box: Box,
    xs: list[float] | list[int] | None = None,
) -> ElementGroup:
    assert xs is None or len(xs) == len(bars)
    elements = ElementGroup()

    # TODO: determine x_width inside this if statement
    # is a little bit hacky
    if xs is None:
        xs = list(range(len(bars)))
        x_width = (max(xs) - min(xs) + 1) / len(xs)
    else:
        x_width = (max(xs) - min(xs)) / len(xs)

    for x, y in zip(xs, bars):
        if y >= 0:
            rect = build_rectangle_from_bottom_center(
                bottom_center=Point(x=x, y=0.0),
                width=0.9 * x_width,
                height=y,
                rounded=0.05,
                classes=["bar"],
                box=chart_box,
            )
        else:
            rect = build_rectangle_from_top_center(
                top_center=Point(x=x, y=0.0),
                width=0.9 * x_width,
                height=y,
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
    step: int,
    font: TTFont = lora,
    title_font_size: int = 32,
    label_font_size: int = 16,
) -> ElementGroup:
    barchart_elements = ElementGroup()

    x_padding = 0.5
    axes = AxesConfig(
        x=build_x_axis_config_barchart(labels=labels),
        # y=build_y_axis_config(values=values, min_value=0),
        y=build_y_axis_config_from_step(values=values, step=step),
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

    bars = build_bars(bars=values, chart_box=chart_box)
    barchart_elements.extend(bars)

    return barchart_elements
