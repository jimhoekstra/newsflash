from typing import Any, Type, Callable, get_type_hints, TypeVar
from inspect import signature

from newsflash.svg.element import Element
from newsflash.endpoints.parsers import RequestValues


class WidgetContainer(Element):
    widget_id: str
    hx_include: list[str] = []
    template: tuple[str, str] = ("widgets", "container.html")


W = TypeVar("W", bound="Widget")


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
        """Performs post-initialization tasks for the widget."""

        self._build_hx_include()
        if self.request_values is not None:
            self._set_values_from_request(self.request_values)

    def query_one(self, type: Type[W], id: str | None = None) -> Type[W]:
        """Queries for a single child widget of the specified type and optional id.

        Parameters
        ----------
        type
            The type of the widget to query.
        id
            The optional id of the widget to query.

        Returns
        -------
        The widget class matching the specified type and id.

        Raises
        ------
        ValueError
            If no widget or multiple widgets are found matching the criteria.
        """
        widgets_of_type = [
            widget for widget in self.children if issubclass(widget, type)
        ]

        if id is None:
            if len(widgets_of_type) == 1:
                return widgets_of_type[0]
            elif len(widgets_of_type) > 1:
                raise ValueError(
                    f"Multiple widgets of type {type} found, please specify an id"
                )
        else:
            for widget in widgets_of_type:
                if widget().id == id:
                    return widget

        raise ValueError(f"Widget not found: {type} with id {id}")

    def get_additional_context(self) -> dict[str, Any]:
        """Returns additional context for rendering the widget.

        In this case it renders all child widgets and includes them in the context.

        Returns
        -------
        A dictionary containing the additional context.
        """
        additional_context = super().get_additional_context()

        children_instances = [child() for child in self.children]
        for child in children_instances:
            child._post_init()

        rendered_children = {child.id: child.render() for child in children_instances}

        additional_context.update({"widgets": rendered_children})
        return additional_context

    def _build_hx_include(self) -> None:
        """Builds the hx-include list based on the callback function's parameters."""

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
        """Sets a single attribute of the widget from the request values.

        Parameters
        ----------
        key
            The attribute name to set.
        inputs
            The request values containing the input data.
        """
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
        """Sets the widget's attributes from the request values.

        Parameters
        ----------
        inputs
            The request values containing the input data.
        """
        for key in self._values_from_request:
            self._set_value_from_request(key, inputs.widget_attributes)

        self.request_values = inputs

    def _get_callback_fn(self) -> Callable | None:
        """Returns the callback function of the current widget if defined, else None.

        Returns
        -------
        The callback function or None.
        """
        callback_fn_name = self._callback_fn_name
        if callback_fn_name is None:
            return None

        callback_fn = getattr(self, callback_fn_name, None)

        assert callback_fn is not None, (
            f"Widget has no callback function '{callback_fn_name}'"
        )

        return callback_fn

    def _get_callback_inputs(self) -> dict[str, "Widget"]:
        """Returns a dictionary of widget instances to be used as inputs for the callback function.

        Returns
        -------
        A dictionary mapping parameter names to widget instances.
        """
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
        """Calls the callback function of the widget and returns the list of widgets to render.

        Returns
        -------
        A list of widgets to render as a result of the callback.
        """
        callback_fn = self._get_callback_fn()
        assert callback_fn is not None, "Widget has no callback function"

        widgets_to_render = callback_fn(**self._get_callback_inputs())
        return widgets_to_render

    def _render_update(self) -> str:
        """Renders the widget for an update after a callback.

        Returns
        -------
        The rendered HTML string of the widget.
        """
        return self.render()
