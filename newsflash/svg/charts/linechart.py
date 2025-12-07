from fontTools.ttLib import TTFont

from newsflash.svg.box import Box
from newsflash.svg.utils import Point
from newsflash.svg.utils.fonts import lora
from newsflash.svg.element import ElementGroup
from newsflash.svg.elements import build_path

from .xy_chart import build_xy_chart
from .axes import AxesConfig, build_x_axis_config, build_y_axis_config


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

    x_padding = len(xs) / 50

    axes = AxesConfig(
        x=build_x_axis_config(values=xs),
        y=build_y_axis_config(values=ys),
    )

    linechart_elements, chart_box = build_xy_chart(
        axes=axes,
        width=width,
        height=height,
        title=title,
        x_padding=x_padding,
        font=font,
        title_font_size=title_font_size,
        label_font_size=label_font_size,
    )

    line = _build_line(xs=xs, ys=ys, chart_box=chart_box)
    linechart_elements.extend(line)

    return linechart_elements
