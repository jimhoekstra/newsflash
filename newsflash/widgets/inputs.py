from typing import Callable

from .widgets import Widget


class Input(Widget):
    template: tuple[str, str] = ("widgets", "input.html")
    value: str = ""

    include_in_context: set[str] = {
        "id",
        "value",
        "hx_include",
        "hx_swap_oob",
        "full_path",
    }

    _values_from_request: list[str] = ["value"]
    _callback_fn_name: str = "on_input"

    def on_input(self, *args, **kwargs) -> list[Widget]:
        """Event handler for input events."""
        return []


class TextArea(Input):
    template: tuple[str, str] = ("widgets", "textarea.html")
    rows: int = 7
    spellcheck: bool = False

    include_in_context: set[str] = {
        "id",
        "hx_include",
        "hx_swap_oob",
        "full_path",
        "value",
        "rows",
        "spellcheck",
    }


class Select(Widget):
    template: tuple[str, str] = ("widgets", "select.html")
    options: list[str] = ["-"]
    selected: str | None = None
    default: Callable[[], str] | None = None

    include_in_context: set[str] = {
        "id",
        "hx_include",
        "hx_swap_oob",
        "full_path",
        "options",
        "selected",
    }

    _callback_fn_name: str = "on_select"
    _values_from_request: list[str] = ["selected"]

    def _post_init(self) -> None:
        if self.selected is None:
            if self.default is not None:
                self.selected = self.default()
            elif len(self.options) > 0:
                self.selected = self.options[0]
            else:
                raise ValueError("Select widget has no options to select from.")

        super()._post_init()

    def on_select(self, *args, **kwargs) -> list[Widget]:
        """Event handler for select events."""
        return []


class Button(Widget):
    template: tuple[str, str] = ("widgets", "button.html")
    label: str = "Click Me"
    hx_include: list[str] = []

    include_in_context: set[str] = {
        "id",
        "hx_include",
        "hx_swap_oob",
        "full_path",
        "label",
    }

    _callback_fn_name: str = "on_click"

    def on_click(self, *args, **kwargs) -> list[Widget]:
        """Event handler for button click events."""
        return []
