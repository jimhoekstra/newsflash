from newsflash.svg.box import Box
from newsflash.svg.utils import Point
from newsflash.svg.utils.fonts import font_size_to_height, lora
from newsflash.svg.elements import build_text, Text, build_line
from newsflash.svg.element import ElementGroup


def build_title_box(width: float, title_font_size: int) -> Box:
    return Box(
        top=0, right=width, bottom=font_size_to_height(title_font_size) * 1.75, left=0
    )


def build_title_text(box: Box, title: str, font_size: int) -> Text:
    return build_text(
        pos=Point(x=0.5, y=0),
        text=title,
        font=lora,
        font_size=font_size,
        horizontal_align="center",
        vertical_align="top",
        box=box,
        classes=["text"],
    )


def _compute_x_axis_height(font_size: int) -> float:
    return font_size_to_height(font_size) * 1.75


def build_y_axis_box(
    min_value: float,
    max_value: float,
    title_box: Box,
    max_label_width: float,
    svg_height: float,
    label_font_size: int,
) -> Box:
    x_axis_height = _compute_x_axis_height(label_font_size)

    return Box(
        top=title_box.bottom,
        right=max_label_width + label_font_size,
        bottom=svg_height - x_axis_height,
        left=0,
        top_y_value=max_value,
        bottom_y_value=min_value,
    )


def build_y_axis(
    y_axis_box: Box,
    font_size: int,
    y_labels: list[float] | list[int],
) -> ElementGroup:
    elements = ElementGroup()

    for y_label in y_labels:
        label = build_text(
            pos=Point(x=0, y=y_label),
            text=str(y_label),
            font=lora,
            font_size=font_size,
            horizontal_align="left",
            vertical_align="middle",
            box=y_axis_box,
            classes=["text"],
        )
        elements.append(label)

    return elements


def build_x_axis_box(
    svg_height: float,
    svg_width: float,
    font_size: int,
    y_axis_box: Box,
    min_x_axis_value: float,
    max_x_axis_value: float,
    padding_left: float = 0.0,
    padding_right: float = 0.0,
) -> Box:
    return Box(
        top=svg_height - _compute_x_axis_height(font_size),
        right=svg_width,
        bottom=svg_height,
        left=y_axis_box.right,
        top_y_value=1.0,
        bottom_y_value=0.0,
        right_x_value=max_x_axis_value,
        left_x_value=min_x_axis_value,
        padding_left=padding_left,
        padding_right=padding_right,
    )


def build_x_axis(
    labels: list[str],
    label_positions: list[float] | list[int],
    font_size: int,
    x_axis_box: Box,
) -> ElementGroup:
    elements = ElementGroup()

    assert len(labels) == len(label_positions)

    for label_position, label_value in zip(label_positions, labels):
        label = build_text(
            pos=Point(x=label_position, y=0),
            text=label_value,
            font=lora,
            font_size=font_size,
            horizontal_align="center",
            vertical_align="bottom",
            box=x_axis_box,
            classes=["text"],
        )
        elements.append(label)

    return elements


def build_chart_box(
    svg_width: float,
    min_x_axis_value: float,
    max_x_axis_value: float,
    min_y_axis_value: float,
    max_y_axis_value: float,
    title_box: Box,
    x_axis_box: Box,
    y_axis_box: Box,
    padding_left: float = 0.0,
    padding_right: float = 0.0,
) -> Box:
    return Box(
        top=title_box.bottom,
        right=svg_width,
        bottom=x_axis_box.top,
        left=y_axis_box.right,
        top_y_value=max_y_axis_value,
        right_x_value=max_x_axis_value,
        bottom_y_value=min_y_axis_value,
        left_x_value=min_x_axis_value,
        padding_left=padding_left,
        padding_right=padding_right,
    )


def build_horizontal_grid_lines(
    y_labels: list[float] | list[int],
    chart_box: Box,
    padding_left: float = 0.0,
    padding_right: float = 0.0,
) -> ElementGroup:
    elements = ElementGroup()

    for y_label in y_labels:
        line = build_line(
            from_pos=Point(x=chart_box.left_x_value - padding_left, y=y_label),
            to_pos=Point(x=chart_box.right_x_value + padding_right, y=y_label),
            box=chart_box,
            classes=["stroke-white", "stroke-rounded", "stroke-width-2", "grid-line"],
        )
        elements.append(line)

    return elements
