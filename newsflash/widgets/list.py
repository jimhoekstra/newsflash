from typing import Any, Type

from newsflash.svg.element import ElementGroup

from .widgets import Widget


class List(Widget):
    template: tuple[str, str] = ("widgets", "list.html")
    element_type: Type[Widget] | None = None
    elements: ElementGroup = ElementGroup()

    def get_additional_context(self) -> dict[str, Any]:
        return {
            "items": [
                {
                    "id": element.id,
                    "content": element.render(),
                }
                for element in self.elements.elements
            ],
        }
