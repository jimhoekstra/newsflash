from typing import TYPE_CHECKING

from fastapi import Request
from newsflash.templates.templates import template_registry
from newsflash.widgets.widgets import Widget
from newsflash.endpoints.parsers import parse_request_values, _parse_url_path

if TYPE_CHECKING:
    from newsflash.app import Page, App


def get_page_callback(page: "Page"):
    async def page_endpoint(request: Request) -> str:
        query_params = request.query_params
        query_params_dict: dict[str, list[str]] = {}
        for k in query_params.keys():
            query_params_dict[k] = query_params.getlist(k)

        page_copy = page.model_copy(
            copy=True,
            query_params=query_params_dict,
        )

        rendered_content = page_copy.render()

        page_template = template_registry.get_template("widgets", "index.html")
        return page_template.render(
            request=request,
            title=page_copy.title,
            content=rendered_content,
        )

    return page_endpoint


def get_callback_endpoint(widget_id: str, app: "App"):
    async def callback_endpoint(request: Request) -> str:
        body = await request.form()
        headers = request.headers

        url_path = _parse_url_path(headers)
        request_values = parse_request_values(body, headers)

        widget = app.get_widget(
            path=url_path,
            type=Widget,
            id=widget_id,
            body_params=request_values,
            # request_values=request_values,
        )

        widgets_to_render = widget._call_callback()

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
