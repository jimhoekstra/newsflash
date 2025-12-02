from fontTools.ttLib import TTFont

from newsflash.svg.box import Box
from newsflash.svg.utils import Point
from newsflash.svg.utils.fonts import lora, get_text_width
from newsflash.svg.element import ElementGroup
from newsflash.svg.elements import build_rectangle_from_bottom_center

from .components import (
    build_title_box,
    build_title_text,
    build_y_axis_box,
    build_y_axis,
    build_x_axis_box,
    build_x_axis,
    build_chart_box,
    build_horizontal_grid_lines,
)


def _build_bars(
    bars: list[float],
    chart_box: Box,
) -> ElementGroup:
    elements = ElementGroup()

    for idx, bar in enumerate(bars):
        rect = build_rectangle_from_bottom_center(
            bottom_center=Point(x=idx / (len(bars) - 1), y=0.0),
            width=0.9 / (len(bars) - 1),
            height=bar,
            rounded=0.05,
            classes=["bar"],
            box=chart_box,
        )
        elements.append(rect)

    return elements


def build_xy_chart(
    labels: list[str],
    x_label_positions: list[float] | list[int],
    y_label_positions: list[float] | list[int],
    width: float,
    height: float,
    title: str,
    max_x_axis_value: float,
    max_y_axis_value: float,
    min_x_axis_value: float = 0.0,
    min_y_axis_value: float = 0.0,
    x_padding: float = 0.0,
    font: TTFont = lora,
    title_font_size: int = 32,
    label_font_size: int = 16,
) -> tuple[ElementGroup, Box]:
    xy_chart_elements = ElementGroup()

    # Title
    title_box = build_title_box(width=width, title_font_size=title_font_size)
    title_text = build_title_text(box=title_box, title=title, font_size=title_font_size)
    xy_chart_elements.append(title_text)

    # Y-Axis
    max_label_width = max(
        [
            get_text_width(font=font, text=str(label), font_size=label_font_size)
            for label in y_label_positions
        ]
    )
    y_axis_box = build_y_axis_box(
        min_value=min_y_axis_value,
        max_value=max_y_axis_value,
        title_box=title_box,
        max_label_width=max_label_width,
        svg_height=height,
        label_font_size=label_font_size,
    )
    y_axis = build_y_axis(
        y_axis_box=y_axis_box, font_size=label_font_size, y_labels=y_label_positions
    )
    xy_chart_elements.extend(y_axis)

    # X-Axis
    x_axis_box = build_x_axis_box(
        svg_height=height,
        svg_width=width,
        font_size=label_font_size,
        y_axis_box=y_axis_box,
        min_x_axis_value=min_x_axis_value,
        max_x_axis_value=max_x_axis_value,
        padding_left=x_padding,
        padding_right=x_padding,
    )
    x_axis = build_x_axis(
        labels=labels,
        label_positions=x_label_positions,
        font_size=label_font_size,
        x_axis_box=x_axis_box,
    )
    xy_chart_elements.extend(x_axis)

    # Chart
    chart_box = build_chart_box(
        svg_width=width,
        min_x_axis_value=min_x_axis_value,
        max_x_axis_value=max_x_axis_value,
        min_y_axis_value=min_y_axis_value,
        max_y_axis_value=max_y_axis_value,
        title_box=title_box,
        x_axis_box=x_axis_box,
        y_axis_box=y_axis_box,
        padding_left=x_padding,
        padding_right=x_padding,
    )
    horizontal_grid_lines = build_horizontal_grid_lines(
        y_labels=y_label_positions,
        chart_box=chart_box,
        padding_left=x_padding,
        padding_right=x_padding,
    )
    xy_chart_elements.extend(horizontal_grid_lines)

    return xy_chart_elements, chart_box
