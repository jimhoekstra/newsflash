from typing import Annotated

from newsflash.svg.utils import Point
from newsflash.svg.box import Box, scale_point_to_box
from newsflash.svg.element import Element, TemplateParam


class Line(Element):
    template: tuple[str, str] = ("svg", "line.svg")
    from_pos: Annotated[Point, TemplateParam()]
    to_pos: Annotated[Point, TemplateParam()]
    stroke_color: Annotated[str, TemplateParam()] = "black"
    stroke_width: Annotated[float, TemplateParam()] = 1.0
    stroke_linecap: Annotated[str, TemplateParam()] = "round"
    path_length: Annotated[float, TemplateParam()] = 1.0


def build_line(
    from_pos: Point,
    to_pos: Point,
    stroke_color: str = "black",
    stroke_width: float = 1.0,
    stroke_linecap: str = "round",
    path_length: float = 1.0,
    box: Box | None = None,
    classes: list[str] = [],
    styles: list[str] = [],
    attributes: dict[str, str] = {},
) -> Line:
    if box is not None:
        from_pos = scale_point_to_box(from_pos, box)
        to_pos = scale_point_to_box(to_pos, box)

    return Line(
        from_pos=from_pos,
        to_pos=to_pos,
        stroke_color=stroke_color,
        stroke_width=stroke_width,
        stroke_linecap=stroke_linecap,
        path_length=path_length,
        classes=classes,
        styles=styles,
        attributes=attributes,
    )
