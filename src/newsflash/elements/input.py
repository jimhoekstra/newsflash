from .base import BaseElement

from newsflash.models import Trigger


class Input(BaseElement):
    name: str = "input"
    template_dir_name: str = "newsflash-elements"
    template_name: str = "input.html"
    placeholder: str = ""
    value: str = ""

    all_triggers: list[str] = ["input"]

    def input(self) -> Trigger:
        return Trigger(
            element_id=self.id,
            element_name=self.name,
            trigger="input",
        )


class InputFloat(BaseElement):
    name: str = "input-float"
    template_dir_name: str = "newsflash-elements"
    template_name: str = "input.html"
    placeholder: str = ""
    value: float = 0.0

    all_triggers: list[str] = ["input"]

    def input(self) -> Trigger:
        return Trigger(
            element_id=self.id,
            element_name=self.name,
            trigger="input",
        )


class InputInteger(BaseElement):
    name: str = "input-integer"
    template_dir_name: str = "newsflash-elements"
    template_name: str = "input.html"
    placeholder: str = ""
    value: int = 0

    all_triggers: list[str] = ["input"]

    def input(self) -> Trigger:
        return Trigger(
            element_id=self.id,
            element_name=self.name,
            trigger="input",
        )
