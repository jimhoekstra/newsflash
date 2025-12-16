from typing import Any, Callable


from .widgets import Widget


class Input(Widget):
    template: tuple[str, str] = ("widgets", "input.html")
    value: str = ""

    _values_from_request: list[str] = ["value"]
    _callback_fn_name: str = "on_input"

    def on_input(self, *args, **kwargs) -> list[Widget]:
        """Event handler for input events."""
        return []


class TextArea(Input):
    template: tuple[str, str] = ("widgets", "textarea.html")
    rows: int = 7
    spellcheck: bool = False


class Select(Widget):
    template: tuple[str, str] = ("widgets", "select.html")
    options: list[str] = ["-"]
    selected: str | None = None
    default: Callable[[], str] | None = None

    _callback_fn_name: str = "on_select"
    _values_from_request: list[str] = ["selected"]

    def model_post_init(self, context: Any) -> None:
        if self.selected is not None:
            return
        if self.default is not None:
            self.selected = self.default()
            return
        if len(self.options) > 0:
            self.selected = self.options[0]
            return

        raise ValueError("Select widget has no options to select from.")

    def on_select(self, *args, **kwargs) -> list[Widget]:
        """Event handler for select events."""
        return []


class Button(Widget):
    template: tuple[str, str] = ("widgets", "button.html")
    label: str = "Click Me"
    hx_include: list[str] = []

    _callback_fn_name: str = "on_click"

    def on_click(self, *args, **kwargs) -> list[Widget]:
        """Event handler for button click events."""
        return []
