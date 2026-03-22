from typing import Annotated

from newsflash.svg.utils import Point
from newsflash.svg.box import Box, scale_point_to_box
from newsflash.svg.element import Element, TemplateParam


class Path(Element):
    template: tuple[str, str] = ("svg", "path.svg")
    points: Annotated[list[Point], TemplateParam()]
    path_length: Annotated[float, TemplateParam()] = 100.0


def build_path(
    points: list[Point],
    path_length: float = 100.0,
    box: Box | None = None,
    classes: list[str] = [],
    styles: list[str] = [],
    attributes: dict[str, str] = {},
) -> Path:
    if box is not None:
        points = [scale_point_to_box(p, box) for p in points]

    return Path(
        points=points,
        path_length=path_length,
        classes=classes,
        styles=styles,
        attributes=attributes,
    )
