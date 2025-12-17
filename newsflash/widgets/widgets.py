from typing import Any, Type, Callable, TypeVar, get_type_hints
from inspect import signature

from newsflash.svg.element import Element
from newsflash.endpoints.parsers import RequestValues


class WidgetContainer(Element):
    widget_id: str
    hx_include: list[str] = []
    template: tuple[str, str] = ("widgets", "container.html")


class Widget(Element):
    hx_include: list[str] = []
    hx_swap_oob: bool = False

    components: list[Type["Widget"]] = []
    request_values: RequestValues | None = None

    _values_from_request: list[str] = []
    _callback_fn_name: str | None = None
    _callback_fn_on_parent: bool = False

    _parent: "Widget | None" = None

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

        self.request_values = inputs

    def get_components(self) -> list[Type["Widget"]]:
        return self.components

    def render(self, additional_context: dict[str, str] | None = None) -> str:
        child_widgets = self.get_components()
        rendered_child_widgets = _build_rendered_widgets(child_widgets)

        return super().render(additional_context=rendered_child_widgets)


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

    if widget._callback_fn_on_parent:
        assert widget._parent is not None, (
            "Widget has no parent to get callback function from"
        )
        parent_widget = widget._parent
        callback_fn = getattr(parent_widget, callback_fn_name, None)
    else:
        callback_fn = getattr(widget, callback_fn_name, None)

    assert callback_fn is not None, (
        f"Widget has no callback function '{callback_fn_name}'"
    )

    return callback_fn


def build_hx_include(callback_fn: Callable) -> list[str]:
    sig = signature(callback_fn)
    parameters = sig.parameters

    type_hints = get_type_hints(callback_fn)

    include_list: list[str] = []
    for param in parameters:
        if param == "self":
            continue
        type_hint = type_hints[param]

        assert issubclass(type_hint, Widget)
        widget_instance = type_hint()
        include_list.append(f"#{widget_instance.id}")

    include_list.append("closest .newsflash-list-item")
    return include_list


def _build_rendered_widgets(widgets: list[Type[Widget]]) -> dict[str, str]:
    rendered_widgets: dict[str, str] = {}

    for widget_cls in widgets:
        widget_instance = widget_cls()

        if (callback_fn := get_widget_callback_fn(widget_instance)) is not None:
            hx_include = build_hx_include(callback_fn)
            widget_instance.hx_include.extend(hx_include)

        rendered_widget = widget_instance.render()

        rendered_widgets[widget_instance.id] = rendered_widget

    return rendered_widgets
