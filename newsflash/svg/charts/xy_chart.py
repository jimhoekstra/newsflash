from fontTools.ttLib import TTFont

from newsflash.svg.box import Box
from newsflash.svg.utils.fonts import lora, get_text_width
from newsflash.svg.element import ElementGroup
from newsflash.svg.utils.fonts import font_size_to_height

from .axes import AxesConfig

from .components import (
    build_title_box,
    build_title_text,
    build_multipler_text,
    build_y_axis_box,
    build_y_axis,
    build_x_axis_box,
    build_x_axis,
    build_chart_box,
    build_horizontal_grid_lines,
)


def build_xy_chart(
    axes: AxesConfig,
    width: float,
    height: float,
    title: str,
    x_padding: float = 0.0,
    font: TTFont = lora,
    title_font_size: int = 32,
    label_font_size: int = 16,
) -> tuple[ElementGroup, Box]:
    xy_chart_elements = ElementGroup()

    # Title
    if title == "":
        title_font_size = label_font_size
    title_box = build_title_box(
        width=width, title_font_size=title_font_size, label_font_size=label_font_size
    )
    title_text = build_title_text(box=title_box, title=title, font_size=title_font_size)
    xy_chart_elements.append(title_text)

    if axes.y.multiplier != 1:
        multiplier_text = build_multipler_text(
            multiplier=axes.y.multiplier,
            font_size=label_font_size,
            box=title_box,
        )
        xy_chart_elements.append(multiplier_text)

    title_spacing_box = Box(
        top=title_box.bottom,
        right=title_box.right,
        bottom=title_box.bottom + font_size_to_height(label_font_size),
        left=title_box.left,
    )

    # Y-Axis
    max_label_width = max(
        [
            get_text_width(font=font, text=str(label), font_size=label_font_size)
            for label in axes.y.labels_as_str
        ]
    )
    y_axis_box = build_y_axis_box(
        min_value=axes.y.min_value,
        max_value=axes.y.max_value,
        title_box=title_spacing_box,
        max_label_width=max_label_width,
        svg_height=height,
        label_font_size=label_font_size,
    )
    y_axis = build_y_axis(
        y_labels=[str(label) for label in axes.y.labels_as_str],
        y_label_positions=axes.y.label_positions,
        font_size=label_font_size,
        y_axis_box=y_axis_box,
    )
    xy_chart_elements.extend(y_axis)

    # X-Axis
    x_axis_box = build_x_axis_box(
        svg_height=height,
        svg_width=width,
        font_size=label_font_size,
        y_axis_box=y_axis_box,
        min_x_axis_value=axes.x.min_value,
        max_x_axis_value=axes.x.max_value,
        padding_left=x_padding,
        padding_right=x_padding,
    )
    x_axis = build_x_axis(
        labels=axes.x.labels_as_str,
        label_positions=axes.x.label_positions,
        font_size=label_font_size,
        x_axis_box=x_axis_box,
    )
    xy_chart_elements.extend(x_axis)

    # Chart
    chart_box = build_chart_box(
        svg_width=width,
        min_x_axis_value=axes.x.min_value,
        max_x_axis_value=axes.x.max_value,
        min_y_axis_value=axes.y.min_value,
        max_y_axis_value=axes.y.max_value,
        title_box=title_spacing_box,
        x_axis_box=x_axis_box,
        y_axis_box=y_axis_box,
        padding_left=x_padding,
        padding_right=x_padding,
    )
    horizontal_grid_lines = build_horizontal_grid_lines(
        y_labels=axes.y.label_positions,
        chart_box=chart_box,
        padding_left=x_padding,
        padding_right=x_padding,
    )
    xy_chart_elements.extend(horizontal_grid_lines)

    return xy_chart_elements, chart_box
