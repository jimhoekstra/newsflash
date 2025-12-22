from typing import Any


from newsflash.svg.element import Element
from newsflash.svg.utils import Point, XCoor, YCoor
from newsflash.svg.box import (
    Box,
    scale_width_to_box,
    scale_height_to_box,
    scale_point_to_box,
)


class Rectangle(Element):
    template: tuple[str, str] = ("svg", "rect.svg")
    top_left: Point
    width: float
    height: float
    rounded: float = 0.0

    include_in_context: set[str] = {
        "top_left",
        "width",
        "height",
        "rounded",
        "classes",
        "styles",
        "attributes",
    }

    @property
    def top(self) -> YCoor:
        return self.top_left.y

    @property
    def right(self) -> XCoor:
        return self.top_left.x + self.width

    @property
    def bottom(self) -> YCoor:
        return self.top_left.y + self.height

    @property
    def left(self) -> XCoor:
        return self.top_left.x

    def get_additional_context(self) -> dict[str, Any]:
        return {
            "rx_ry": self.rounded * self.width,
        }


def build_rectangle(
    top_left: Point,
    width: float,
    height: float,
    rounded: float = 0.0,
    box: Box | None = None,
    classes: list[str] = [],
    styles: list[str] = [],
    attributes: dict[str, str] = {},
) -> Rectangle:
    if box is not None:
        top_left = scale_point_to_box(top_left, box)
        width = scale_width_to_box(width, box)
        height = scale_height_to_box(height, box)

    return Rectangle(
        top_left=top_left,
        width=width,
        height=height,
        rounded=rounded,
        classes=classes,
        styles=styles,
        attributes=attributes,
    )


def build_rectangle_from_bottom_center(
    bottom_center: Point,
    width: float,
    height: float,
    rounded: float = 0.0,
    box: Box | None = None,
    classes: list[str] = [],
    styles: list[str] = [],
    attributes: dict[str, str] = {},
) -> Rectangle:
    if box is not None:
        bottom_center = scale_point_to_box(bottom_center, box)
        width = scale_width_to_box(width, box)
        height = scale_height_to_box(height, box)

    top_left = Point(
        x=bottom_center.x - width / 2,
        y=bottom_center.y - height,
    )

    return Rectangle(
        top_left=top_left,
        width=width,
        height=height,
        rounded=rounded,
        classes=classes,
        styles=styles,
        attributes=attributes,
    )


def build_background_rectangle(
    box: Box,
    classes: list[str] = [],
    styles: list[str] = [],
    attributes: dict[str, str] = {},
) -> Rectangle:
    box = box.apply_padding()
    return build_rectangle(
        top_left=Point(x=box.left_x_value, y=box.top_y_value),
        width=abs(box.right_x_value - box.left_x_value),
        height=abs(box.bottom_y_value - box.top_y_value),
        box=box,
        classes=classes,
        styles=styles,
        attributes=attributes,
    )
