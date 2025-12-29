from typing import Any, Type, Callable, get_type_hints, TypeVar
from inspect import signature

from newsflash.svg.element import Element
from newsflash.endpoints.parsers import RequestValues


class WidgetContainer(Element):
    widget_id: str
    hx_include: list[str] = []
    template: tuple[str, str] = ("widgets", "container.html")

    include_in_context: set[str] = {
        "widget_id",
        "full_path",
        "hx_include",
    }


W = TypeVar("W", bound="Widget")


class Widget(Element):
    hx_include: list[str] = []
    hx_swap_oob: bool = False

    children: list["Widget"] = []
    parent: "Widget | None" = None
    request_values: RequestValues | None = None

    _values_from_request: list[str] = []
    _include_parent: bool = False
    _callback_fn_name: str | None = None
    _callback_fn_on_parent: bool = False

    _parent: "Widget | None" = None

    def _make_copy(self: W, update: dict[str, Any] = {}) -> W:
        widget_copy = self.model_copy(update=update)
        widget_copy._post_init()
        return widget_copy

    def _post_init(self) -> None:
        self._build_hx_include()
        if self.request_values is not None:
            self._set_values_from_request(self.request_values)

    def get_child_widget(
        self,
        type: Type[W],
        id: str,
        request_values: RequestValues | None = None,
    ) -> W:
        widgets_of_type = [
            widget for widget in self.children if isinstance(widget, type)
        ]

        id_split = id.split("/")

        if len(id_split) == 1:
            for widget in widgets_of_type:
                if widget.id == id:
                    widget_copy = widget._make_copy(
                        update={
                            "request_values": request_values,
                            "parent": self,
                        }
                    )
                    return widget_copy

        remaining_id = "/".join(id_split[1:])
        for widget in widgets_of_type:
            if widget.id == id_split[0]:
                widget_copy = widget._make_copy(
                    update={
                        "request_values": request_values,
                        "parent": self,
                    }
                )

                widget_copy._post_init()

                return widget_copy.get_child_widget(
                    type=type,
                    id=remaining_id,
                    request_values=request_values,
                )

        raise ValueError(f"Widget not found: {type} with id {id}")

    @property
    def full_path(self) -> str:
        if self.parent is not None:
            full_path = f"{self.parent.full_path}/{self.id}"
        else:
            full_path = self.id

        full_path = full_path.strip("/")

        return full_path

    @property
    def root_widget(self) -> "Widget":
        if self.parent is None:
            return self
        else:
            return self.parent.root_widget

    def get_additional_context(self) -> dict[str, Any]:
        additional_context = super().get_additional_context()

        for child in self.children:
            child.parent = self

        children_instances = [child._make_copy() for child in self.children]
        rendered_children = {child.id: child.render() for child in children_instances}

        additional_context.update({"widgets": rendered_children})
        additional_context.update({"widget_list": list(rendered_children.values())})
        additional_context.update({"full_path": self.full_path})

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

        if self._include_parent and self.parent is not None:
            include_list.append(f"#{self.parent.id}")

        self.hx_include = include_list

    def _set_value_from_request(self, key: str, inputs: dict[str, Any]) -> None:
        current_value = getattr(self, key, None)
        assert current_value is not None, f"Widget has no attribute '{key}'"

        value_type = type(current_value)
        value = inputs.get(f"{self.id}-{key}", None)

        if value is not None:
            assert isinstance(value, value_type), (
                f"Expected type {value_type} for key '{key}', got {type(value)}"
            )
            setattr(self, key, value)

    def _set_values_from_request(self, inputs: RequestValues) -> None:
        attributes = {
            k: v
            for k, v in inputs.widget_attributes.items()
            if k.startswith(f"{self.id}-")
        }

        for key in self._values_from_request:
            self._set_value_from_request(key, attributes)

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

            # TODO: determine correct parent for the widget
            widget_instance = widget_class(request_values=self.request_values, parent=self.root_widget)
            
            widget_instance._post_init()
            input_dict[param] = widget_instance

        return input_dict

    def _call_callback(self) -> list["Widget"]:
        callback_fn = self._get_callback_fn()
        assert callback_fn is not None, "Widget has no callback function"

        widgets_to_render = callback_fn(**self._get_callback_inputs())
        return widgets_to_render

    def _render_update(self) -> str:
        self.hx_swap_oob = True
        return self.render()
