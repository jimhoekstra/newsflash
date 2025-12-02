from jinja2 import Template

from newsflash.svg.element import ElementGroup
from newsflash.svg.templates import svg_templates


class SVG(ElementGroup):
    template: Template = svg_templates.get_template("svg.svg")
    width: float
    height: float
    hx_swap_oob: bool = False
