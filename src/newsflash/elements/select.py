import typing

from .base import BaseElement

from newsflash.models import (
    Trigger,
    FunctionDefinition,
    FunctionInputDefinition,
    Element,
)


class Select(BaseElement):
    name: str = "select"
    template_dir_name: str = "newsflash-elements"
    template_name: str = "select.html"

    value: str = ""
    options: list[str] = []

    all_triggers: list[str] = ["search", "select"]

    def search(self) -> Trigger:
        return Trigger(
            element_id=self.id,
            element_name=self.name,
            trigger="search",
        )

    def select(self) -> Trigger:
        return Trigger(
            element_id=self.id,
            element_name=self.name,
            trigger="select",
        )

    def with_options(self, options: list[str] | list[int] | list[float]) -> typing.Self:
        self.options = [str(x) for x in options]
        return self

    def _get_default_functions(self) -> typing.Iterable[FunctionDefinition]:
        def refresh_after_select(select_element: Select) -> typing.Iterable[Element]:
            yield select_element

        return [
            FunctionDefinition(
                func=refresh_after_select,
                triggers=[self.select()],
                inputs=[
                    FunctionInputDefinition(
                        arg_name="select_element",
                        element_type=self.__class__,
                        element_id=self.id,
                    )
                ],
            )
        ]
