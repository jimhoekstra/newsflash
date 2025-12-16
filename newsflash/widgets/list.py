from typing import Any

from newsflash.svg.element import Element, ElementGroup

from .widgets import Widget


class List(Widget):
    template: tuple[str, str] = ("widgets", "list.html")
    elements: ElementGroup = ElementGroup()

    def get_additional_context(self) -> dict[str, Any]:
        rendered_elements = [element.render() for element in self.elements.elements]
        print("list additional context:", rendered_elements)
        return {
            "items": rendered_elements,
        }
