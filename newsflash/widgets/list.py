from typing import Any

from jinja2 import Template
from pydantic import BaseModel

from newsflash.svg.element import ElementGroup
from newsflash.widgets.widgets import WidgetContainer
from newsflash.templates.templates import get_template

from .widgets import Widget


class List(Widget):
    
    template: tuple[str, str] = ("widgets", "list.html")
    elements: ElementGroup = ElementGroup()

    def render_container(self) -> str:
        container = WidgetContainer(
            widget_id=self.id,
        )
        return container.render()

    def get_additional_context(self) -> dict[str, Any]:
        list_item_template = get_template("widgets", "list_item.html")
        rendered_elements = [
            list_item_template.render({"item": element.render()})
            for element in self.elements.elements
        ]
        return {
            "content": "\n    ".join(rendered_elements),
        }
