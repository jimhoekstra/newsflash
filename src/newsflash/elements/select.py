import typing

from .base import BaseElement

from newsflash.models import Trigger


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
