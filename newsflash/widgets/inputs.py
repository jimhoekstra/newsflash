from jinja2 import Template

from newsflash.widgets.templates import widget_templates

from .widgets import Widget


class Input(Widget):
    template: Template = widget_templates.get_template("input.html")
    value: str = ""

    _values_from_request: list[str] = ["value"]
    _callback_fn_name: str = "on_input"

    def on_input(self, *args, **kwargs) -> list[Widget]:
        """Event handler for input events."""
        return []


class TextArea(Input):
    template: Template = widget_templates.get_template("textarea.html")
    rows: int = 7
    spellcheck: bool = False


class Select(Widget):
    template: Template = widget_templates.get_template("select.html")
    options: list[str] = ["-"]
    selected: str = "-"

    _callback_fn_name: str = "on_select"
    _values_from_request: list[str] = ["selected"]

    def on_select(self, *args, **kwargs) -> list[Widget]:
        """Event handler for select events."""
        return []


class Button(Widget):
    template: Template = widget_templates.get_template("button.html")
    label: str = "Click Me"
    hx_include: list[str] = []

    _callback_fn_name: str = "on_click"

    def on_click(self, *args, **kwargs) -> list[Widget]:
        """Event handler for button click events."""
        return []
