from .input import Input

from newsflash.models import Trigger


class Select(Input):
    name: str = "select"
    template_dir_name: str = "newsflash-elements"
    template_name: str = "select.html"

    options: list[str] = []
    selected: str = ""

    all_triggers: list[str] = ["input", "select", "revealed"]

    def input(self) -> Trigger:
        return Trigger(
            element_id=self.id,
            element_name=self.name,
            trigger="input",
        )

    def select(self) -> Trigger:
        return Trigger(
            element_id=self.id,
            element_name=self.name,
            trigger="select",
        )

    def revealed(self) -> Trigger:
        return Trigger(
            element_id=self.id,
            element_name=self.name,
            trigger="revealed",
        )
