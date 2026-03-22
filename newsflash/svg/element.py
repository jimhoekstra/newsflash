from typing import Any, Annotated

from pydantic import BaseModel, ConfigDict

from newsflash.templates.templates import template_registry


class TemplateParam:
    template_param_name: str | None = None

    def __init__(self, template_param_name: str | None = None) -> None:
        self.template_param_name = template_param_name

    def get_template_param_name(self) -> str | None:
        return self.template_param_name


class Element(BaseModel):
    template: tuple[str, str] | None = None
    id: Annotated[str, TemplateParam()] = ""

    classes: Annotated[list[str], TemplateParam()] = []
    styles: Annotated[list[str], TemplateParam()] = []
    attributes: Annotated[dict[str, str], TemplateParam()] = {}

    model_config = ConfigDict(arbitrary_types_allowed=True, validate_assignment=True)

    def _get_all_template_params(self) -> dict[str, Any]:
        template_params: dict[str, Any] = {}

        for k, v in self.__class__.model_fields.items():
            if len(v.metadata) == 0:
                continue

            if p := next((m for m in v.metadata if isinstance(m, TemplateParam)), None):
                template_param_name = p.get_template_param_name() or k
                template_params[template_param_name] = getattr(self, k)

        return template_params

    def get_additional_context(self) -> dict[str, Any]:
        return {}

    def render(self, additional_context: dict[str, Any] = {}) -> str:
        context = self._get_all_template_params()
        context.update(self.get_additional_context())
        context.update(additional_context)

        assert self.template is not None, (
            f"Element with ID '{self.id}' has no template defined"
        )

        template = template_registry.get_template(
            template_folder=self.template[0], template_name=self.template[1]
        )

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
