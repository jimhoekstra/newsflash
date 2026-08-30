from .base import Element

from newsflash.models import Trigger


class Button(Element):
    name: str = "button"
    label: str = "Button"
    template_dir_name: str = "newsflash-elements"
    template_name: str = "button.html"

    all_triggers: list[str] = ["click"]

    def click(self) -> Trigger:
        return Trigger(
            element_id=self.id,
            element_name=self.name,
            trigger="click",
        )
