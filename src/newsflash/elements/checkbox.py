from typing import Any

from .base import BaseElement

from newsflash.models import Trigger


class Checkbox(BaseElement):
    name: str = "checkbox"
    template_dir_name: str = "newsflash-elements"
    template_name: str = "checkbox.html"

    value: str | None = None
    checked: bool = False
    label: str = ""

    all_triggers: list[str] = ["click"]

    def model_post_init(self, context: Any) -> None:
        if self.value == "on":
            self.checked = True
        elif self.value is None:
            self.checked = False
        else:
            raise ValueError("unexpected `value` for checkbox")

        return super().model_post_init(context)

    def click(self) -> Trigger:
        return Trigger(
            element_id=self.id,
            element_name=self.name,
            trigger="click",
        )
