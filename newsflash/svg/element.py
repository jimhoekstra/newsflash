from typing import Any

from pydantic import BaseModel, ConfigDict
from fastapi import Request

from newsflash.templates.templates import template_registry


class Element(BaseModel):
    template: tuple[str, str] | None = None
    id: str = ""

    include_in_context: set[str] = set()

    classes: list[str] = []
    styles: list[str] = []
    attributes: dict[str, str] = {}

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def get_additional_context(self) -> dict[str, Any]:
        return {}

    def modify_context(self, context: dict[str, Any]) -> dict[str, Any]:
        return context

    def render(
        self,
        request: Request | None = None,
        additional_context: dict[str, Any] | None = None,
    ) -> str:
        context = self.model_dump(include=self.include_in_context)

        if request is not None:
            context["request"] = request
        context.update(self.get_additional_context())

        if additional_context is not None:
            context.update(additional_context)

        assert self.template is not None, (
            f"Element with ID '{self.id}' has no template defined"
        )

        template = template_registry.get_template(
            template_folder=self.template[0], template_name=self.template[1]
        )

        context = self.modify_context(context)
        rendered = template.render(context)
        return rendered


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
