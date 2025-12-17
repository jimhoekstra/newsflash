from typing import Callable, get_type_hints, Awaitable, TYPE_CHECKING
from inspect import signature

from fastapi import Request

from newsflash.widgets.widgets import Widget, widget_factory, get_widget_callback_fn
from .parsers import parse_request_values, RequestValues
from .page import build_hx_include

if TYPE_CHECKING:
    # Only import for type checking to avoid circular imports
    from newsflash.app import App


def build_callback_endpoint(app: "App") -> Callable[..., Awaitable[str]]:
    async def callback_endpoint(request: Request, widget_id: str) -> str:
        body = await request.form()
        headers = request.headers
        request_values = parse_request_values(body, headers)

        chart_element = app.query_one(
            path=request_values.url_path, type=Widget, id=widget_id
        )

        widget_instance = chart_element()
        widget_instance._set_values_from_request(request_values)

        if widget_instance._parent is not None:
            assert widget_instance._parent is not None, "CompositeWidget has no parent"
            widget_instance._parent._set_values_from_request(request_values)

        callback_fn = get_widget_callback_fn(widget_instance)
        assert callback_fn is not None, "Widget has no callback function"
        callback_inputs = _get_callback_inputs(
            callback_fn=callback_fn,
            request_values=request_values,
        )

        widgets_to_render = callback_fn(**callback_inputs)

        rendered_widgets = []
        assert isinstance(widgets_to_render, list), (
            "Callback must return a list of widgets"
        )
        for widget in widgets_to_render:
            assert isinstance(widget, Widget), "Callback must return a list of widgets"
            widget.hx_swap_oob = True

            if (callback_fn := get_widget_callback_fn(widget)) is not None:
                hx_include = build_hx_include(callback_fn)
                widget.hx_include.extend(hx_include)

            rendered_widgets.append(widget.render())

        return "\n".join(rendered_widgets)

    return callback_endpoint


def _get_callback_inputs(
    callback_fn: Callable,
    request_values: RequestValues,
) -> dict[str, Widget]:
    sig = signature(callback_fn)
    parameters = sig.parameters

    type_hints = get_type_hints(callback_fn)

    input_dict = {}
    for param in parameters:
        if param == "self":
            continue
        widget_class = type_hints.get(param, "Unknown")
        assert issubclass(widget_class, Widget)

        widget_instance = widget_factory(widget_class, request_values=request_values)
        input_dict[param] = widget_instance

    return input_dict
