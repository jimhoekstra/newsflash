import polars as pl

from fontTools.ttLib import TTFont

from newsflash.svg.utils.fonts import lora
from newsflash.svg.element import ElementGroup

from .xy_chart import build_xy_chart
from .axes import (
    AxesConfig,
    build_y_axis_config,
    build_spaced_x_axis_config,
)
from .barchart import build_bars


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

    bars = build_bars(bars=ys, chart_box=chart_box, xs=xs)
    barchart_elements.extend(bars)

    return barchart_elements
