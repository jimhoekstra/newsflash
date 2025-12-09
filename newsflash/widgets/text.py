from jinja2 import Template

from .templates import widget_templates
from .widgets import Widget


class ValueDisplay(Widget):
    template: Template = widget_templates.get_template("value_display.html")
    label: str = ""
    value: str = ""

    _values_from_request: list[str] = ["value"]
