from .base import Trigger
from .input import Input


class Select(Input):
    name: str = "select"
    template_dir_name: str = "newsflash-elements"
    template_name: str = "select.html"
    
    options: list[str] = []
    selected: str = ""

    _all_triggers: list[str] = ["input", "select", "revealed"]

    def input(self) -> Trigger:
        return Trigger(
            element=self,
            trigger="input",
        )

    def select(self) -> Trigger:
        return Trigger(
            element=self,
            trigger="select",
        )

    def revealed(self) -> Trigger:
        return Trigger(
            element=self,
            trigger="revealed",
        )
