from typing import Any, Type, Callable, TypeVar

from jinja2 import Template

from newsflash.svg.element import Element
from newsflash.widgets.templates import widget_templates
from newsflash.endpoints.parsers import RequestValues


class WidgetContainer(Element):
    widget_id: str
    hx_include: list[str] = []
    template: Template = widget_templates.get_template("container.html")


class Widget(Element):
    hx_include: list[str] = []
    hx_swap_oob: bool = False

    _values_from_request: list[str] = []
    _callback_fn_name: str | None = None

    def _set_value_from_request(self, key: str, inputs: dict[str, Any]) -> None:
        current_value = getattr(self, key, None)
        assert current_value is not None, f"Widget has no attribute '{key}'"

        value_type = type(current_value)
        value = inputs.get(f"{self.id}-{key}", None)

        assert value is not None, f"No value provided for key '{key}'"
        assert isinstance(value, value_type), (
            f"Expected type {value_type} for key '{key}', got {type(value)}"
        )
        setattr(self, key, value)

    def _set_values_from_request(self, inputs: RequestValues) -> None:
        for key in self._values_from_request:
            self._set_value_from_request(key, inputs.widget_attributes)

W = TypeVar("W", bound=Widget)


def widget_factory(widget_class: Type[W], request_values: RequestValues) -> W:
    widget_instance = widget_class()
    widget_instance._set_values_from_request(request_values)
    return widget_instance


def get_widget_callback_fn(
    widget: Widget,
) -> Callable | None:
    callback_fn_name = widget._callback_fn_name
    if callback_fn_name is None:
        return None

    callback_fn = getattr(widget, callback_fn_name, None)
    assert callback_fn is not None, (
        f"Widget has no callback function '{callback_fn_name}'"
    )

    return callback_fn
