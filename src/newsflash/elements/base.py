import typing

from newsflash.models import Element
from newsflash.templates import template_registry


class BaseElement(Element):
    def render(
        self,
        trigger_context_getter: typing.Callable[
            [str, list[str]], dict[str, str | bool]
        ],
        hx_swap_oob: str | None,
    ) -> str:
        template = template_registry.get_template(
            dir_name=self.template_dir_name,
            template_file_name=self.template_name,
        )

        trigger_context = trigger_context_getter(self.id, self.all_triggers)

        rendered = template.render(
            {
                **self.model_dump(exclude={"_children"}),
                "hx_swap_oob": hx_swap_oob,
                "elements": {
                    element.id: element.render(
                        trigger_context_getter=trigger_context_getter, hx_swap_oob=None
                    )
                    for element in self.compose()
                },
                **trigger_context,
            }
        )

        return rendered

    def compose(self) -> typing.Iterable["Element"]:
        yield from self.children
