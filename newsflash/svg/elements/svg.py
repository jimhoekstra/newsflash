from jinja2 import Template

from newsflash.svg.element import ElementGroup


class SVG(ElementGroup):
    template: tuple[str, str] = ("svg", "svg.svg")
    width: float
    height: float
    hx_swap_oob: bool = False
