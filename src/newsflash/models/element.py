import typing
from abc import ABC, abstractmethod

from pydantic import BaseModel


class Element(BaseModel, ABC):

    id: str
    name: str
    template_dir_name: str
    template_name: str

    children: list["Element"] = []

    all_triggers: list[str] = []

    @abstractmethod
    def render(
        self, 
        trigger_context_getter: typing.Callable[[str, list[str]], dict[str, str | bool]],
        hx_swap_oob: str | None,
    ) -> str:
        ...

    @abstractmethod
    def compose(self) -> typing.Iterable["Element"]:
        ...
