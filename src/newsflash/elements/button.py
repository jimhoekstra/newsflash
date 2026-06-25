from .base import Element, Trigger


class Button(Element):
    name: str = "button"
    label: str = "Button"
    template_dir_name: str = "newsflash-elements"
    template_name: str = "button.html"

    def click(self) -> Trigger:
        return Trigger(
            element=self,
            trigger="click",
        )
