from typing import Literal, Annotated

from fontTools.ttLib import TTFont

from newsflash.svg.element import Element, TemplateParam
from newsflash.svg.utils import Point, XCoor, YCoor
from newsflash.svg.box import Box, scale_point_to_box
from newsflash.svg.utils.fonts import get_text_width


type HorizontalAlign = Literal["left", "center", "right"]
type VerticalAlign = Literal["top", "middle", "default", "bottom"]


class Text(Element):
    template: tuple[str, str] = ("svg", "text.svg")
    pos: Annotated[Point, TemplateParam()]
    text: Annotated[str, TemplateParam()]
    width: Annotated[float, TemplateParam()]
    font_size: Annotated[int, TemplateParam()]

    @property
    def top(self) -> YCoor:
        return self.pos.y - self.font_size

    @property
    def right(self) -> XCoor:
        return self.pos.x + self.width

    @property
    def bottom(self) -> YCoor:
        return self.pos.y + self.font_size / 3

    @property
    def left(self) -> XCoor:
        return self.pos.x

    @property
    def height(self) -> float:
        return self.font_size * 4 / 3


def build_text(
    pos: Point,
    text: str,
    font: TTFont,
    font_size: int,
    horizontal_align: HorizontalAlign = "left",
    vertical_align: VerticalAlign = "default",
    box: Box | None = None,
    classes: list[str] = [],
    styles: list[str] = [],
    attributes: dict[str, str] = {},
) -> Text:
    if box is not None:
        pos = scale_point_to_box(pos, box)

    text_width = get_text_width(font, text, font_size)
    if horizontal_align == "center":
        pos.x = pos.x - text_width / 2
    elif horizontal_align == "right":
        pos.x = pos.x - text_width

    if vertical_align == "top":
        pos.y = pos.y + font_size
    elif vertical_align == "middle":
        pos.y = pos.y + font_size / 4
    elif vertical_align == "bottom":
        pos.y = pos.y - font_size / 4

    styles = styles + [f"font-size: {font_size}px;"]

    return Text(
        pos=pos,
        text=text,
        width=text_width,
        font_size=font_size,
        classes=classes,
        styles=styles,
        attributes=attributes,
    )
