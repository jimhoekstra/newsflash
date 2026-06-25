from .base import Element, Trigger


class Input(Element):
    name: str = "input"
    template_dir_name: str = "newsflash-elements"
    template_name: str = "input.html"
    placeholder: str = ""
    value: str = ""

    def input(self) -> Trigger:
        return Trigger(
            element=self,
            trigger="input",
        )


class InputFloat(Element):
    name: str = "input-float"
    template_dir_name: str = "newsflash-elements"
    template_name: str = "input.html"
    placeholder: str = ""
    value: float = 0.0

    def input(self) -> Trigger:
        return Trigger(
            element=self,
            trigger="input",
        )


class InputInteger(Element):
    name: str = "input-integer"
    template_dir_name: str = "newsflash-elements"
    template_name: str = "input.html"
    placeholder: str = ""
    value: int = 0

    def input(self) -> Trigger:
        return Trigger(
            element=self,
            trigger="input",
        )
