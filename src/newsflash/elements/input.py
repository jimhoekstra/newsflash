from .base import Element, Trigger


class Input(Element):
    name: str = "input"
    template_dir_name: str = "newsflash-elements"
    template_name: str = "input.html"
    placeholder: str = ""
    value: str = ""

    _all_triggers: list[str] = ["input"]

    def input(self) -> Trigger:
        return Trigger(
            element_id=self.id,
            element_name=self.name,
            trigger="input",
        )


class InputFloat(Element):
    name: str = "input-float"
    template_dir_name: str = "newsflash-elements"
    template_name: str = "input.html"
    placeholder: str = ""
    value: float = 0.0

    _all_triggers: list[str] = ["input"]

    def input(self) -> Trigger:
        return Trigger(
            element_id=self.id,
            element_name=self.name,
            trigger="input",
        )


class InputInteger(Element):
    name: str = "input-integer"
    template_dir_name: str = "newsflash-elements"
    template_name: str = "input.html"
    placeholder: str = ""
    value: int = 0

    _all_triggers: list[str] = ["input"]

    def input(self) -> Trigger:
        return Trigger(
            element_id=self.id,
            element_name=self.name,
            trigger="input",
        )
