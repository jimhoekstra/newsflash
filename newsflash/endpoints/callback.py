from typing import Callable, Awaitable, TYPE_CHECKING

from fastapi import Request

from newsflash.widgets.widgets import Widget
from .parsers import parse_request_values

if TYPE_CHECKING:
    # Only import for type checking to avoid circular imports
    from newsflash.app import App


def build_callback_endpoint(app: "App") -> Callable[..., Awaitable[str]]:
    async def callback_endpoint(request: Request, widget_id: str) -> str:
        body = await request.form()
        headers = request.headers
        request_values = parse_request_values(body, headers)

        element = app.query_one(path=request_values.url_path, type=Widget, id=widget_id)

        widget_instance = element(request_values=request_values)
        widget_instance._post_init()
        widgets_to_render = widget_instance._call_callback()

        rendered_widgets = []
        assert isinstance(widgets_to_render, list), (
            "Callback must return a list of widgets"
        )
        for widget in widgets_to_render:
            assert isinstance(widget, Widget), "Callback must return a list of widgets"
            widget.hx_swap_oob = True
            rendered_widgets.append(widget._render_update())

        return "\n".join(rendered_widgets)

    return callback_endpoint
