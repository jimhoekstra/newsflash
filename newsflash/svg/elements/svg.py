from typing import Annotated

from newsflash.svg.element import ElementGroup, TemplateParam


class SVG(ElementGroup):
    template: tuple[str, str] = ("svg", "svg.svg")
    width: Annotated[float, TemplateParam()]
    height: Annotated[float, TemplateParam()]
    hx_swap_oob: Annotated[bool, TemplateParam()] = False
