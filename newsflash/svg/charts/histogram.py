import polars as pl

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
    build_spaced_x_axis_config,
)


def _build_bars(
    bars: list[float] | list[int],
    chart_box: Box,
    xs: list[float] | list[int] | None = None,
) -> ElementGroup:
    assert xs is None or len(xs) == len(bars)
    elements = ElementGroup()

    if xs is None:
        xs = list(range(len(bars)))

    x_width = (max(xs) - min(xs)) / len(xs)

    for x, y in zip(xs, bars):
        rect = build_rectangle_from_bottom_center(
            bottom_center=Point(x=x, y=0.0),
            width=0.9 * x_width,
            height=y,
            rounded=0.05,
            classes=["bar"],
            box=chart_box,
        )
        elements.append(rect)

    return elements


def build_histogram(
    values: list[float] | list[int],
    num_bins: int,
    width: float,
    height: float,
    title: str,
    font: TTFont = lora,
    title_font_size: int = 32,
    label_font_size: int = 16,
) -> ElementGroup:
    values_hist = pl.Series(values).hist(bin_count=num_bins)
    barchart_elements = ElementGroup()

    xs = values_hist.get_column("breakpoint").to_list()
    ys = values_hist.get_column("count").to_list()

    x_width = (max(xs) - min(xs)) / len(xs)
    x_padding = x_width / 2

    axes = AxesConfig(
        x=build_spaced_x_axis_config(values=xs),
        y=build_y_axis_config(values=ys, min_value=0),
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

    bars = _build_bars(bars=ys, chart_box=chart_box, xs=xs)
    barchart_elements.extend(bars)

    return barchart_elements
