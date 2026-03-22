from typing import Annotated

from .widgets import Widget
from newsflash.svg.element import TemplateParam


class HTML(Widget):
    template: tuple[str, str] = ("widgets", "html.html")
    html_content: Annotated[str, TemplateParam()] = ""
    