from .input import Input

from newsflash.models import Trigger


class Textarea(Input):
    name: str = "textarea"
    template_dir_name: str = "newsflash-elements"
    template_name: str = "textarea.html"
    rows: int | None = None
    cols: int | None = None
    placeholder: str = ""
    value: str = ""

    all_triggers: list[str] = ["input"]

    def input(self) -> Trigger:
        return Trigger(
            element_id=self.id,
            element_name=self.name,
            trigger="input",
        )
