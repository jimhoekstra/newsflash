from typing import Any

from pydantic import BaseModel, ConfigDict

from newsflash.templates.templates import get_template


class Element(BaseModel):
    template: tuple[str, str] | None = None
    id: str = ""
    classes: list[str] = []
    styles: list[str] = []
    attributes: dict[str, str] = {}

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def get_additional_context(self) -> dict[str, str]:
        return {}

    def render(self) -> str:
        context = self.model_dump()
        context.update(self.get_additional_context())
        assert self.template is not None, "Template is not set."

        template = get_template(template_folder=self.template[0], template_name=self.template[1])
        return template.render(context)


class ElementGroup(Element):
    elements: list[Element] = []

    def append(self, element: Element) -> None:
        self.elements.append(element)

    def extend(self, other: "ElementGroup") -> None:
        self.elements.extend(other.elements)

    def get_additional_context(self) -> dict[str, Any]:
        return {
            "content": "\n    ".join(element.render() for element in self.elements),
        }
