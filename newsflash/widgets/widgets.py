from typing import Any, Type, Callable, get_type_hints
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

    children: list[Type["Widget"]] = []
    request_values: RequestValues | None = None

    _values_from_request: list[str] = []
    _callback_fn_name: str | None = None
    _callback_fn_on_parent: bool = False

    _parent: "Widget | None" = None

    def _post_init(self) -> None:
        self._build_hx_include()
        if self.request_values is not None:
            self._set_values_from_request(self.request_values)

    def get_additional_context(self) -> dict[str, Any]:
        additional_context = super().get_additional_context()

        children_instances = [child() for child in self.children]
        for child in children_instances:
            child._post_init()

        rendered_children = {child.id: child.render() for child in children_instances}

        additional_context.update({"widgets": rendered_children})
        return additional_context

    def _build_hx_include(self) -> None:
        callback_fn = self._get_callback_fn()
        if callback_fn is None:
            return

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

        self.hx_include = include_list

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

    def _get_callback_fn(self) -> Callable | None:
        callback_fn_name = self._callback_fn_name
        if callback_fn_name is None:
            return None

        callback_fn = getattr(self, callback_fn_name, None)

        assert callback_fn is not None, (
            f"Widget has no callback function '{callback_fn_name}'"
        )

        return callback_fn

    def _get_callback_inputs(self) -> dict[str, "Widget"]:
        callback_fn = self._get_callback_fn()
        assert callback_fn is not None, "Widget has no callback function"
        assert self.request_values is not None, "Widget has no request values"

        sig = signature(callback_fn)
        parameters = sig.parameters

        type_hints = get_type_hints(callback_fn)

        input_dict = {}
        for param in parameters:
            if param == "self":
                continue
            widget_class = type_hints.get(param, "Unknown")
            assert issubclass(widget_class, Widget)

            widget_instance = widget_class(request_values=self.request_values)
            widget_instance._post_init()
            input_dict[param] = widget_instance

        return input_dict

    def _call_callback(self) -> list["Widget"]:
        callback_fn = self._get_callback_fn()
        assert callback_fn is not None, "Widget has no callback function"

        widgets_to_render = callback_fn(**self._get_callback_inputs())
        return widgets_to_render

    def _render_update(self) -> str:
        return self.render()
