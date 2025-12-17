from typing import Type, Callable, get_type_hints, Awaitable
from inspect import signature

from fastapi import Request
from fastapi.templating import Jinja2Templates
from jinja2 import Template

from newsflash.widgets.charts import Chart
from newsflash.widgets.widgets import Widget, get_widget_callback_fn
from newsflash.templates.templates import get_template


def build_page_endpoint(
    page_title: str,
    page_template_name: str,
    widgets: list[Type[Widget]],
    templates: Jinja2Templates,
) -> Callable[..., Awaitable[str]]:
    async def read_page(request: Request) -> str:
        rendered_widgets: dict[str, str] = _build_rendered_widgets(widgets)

        template: Template = templates.get_template(page_template_name)
        rendered_content = template.render(
            request=request,
            widgets=rendered_widgets,
        )

        page_template = get_template("widgets", "index.html")
        return page_template.render(
            request=request,
            title=page_title,
            content=rendered_content,
        )

    return read_page


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

        if isinstance(widget_instance, Chart):
            rendered_widget = widget_instance.render_container()
        else:
            rendered_widget = widget_instance.render()

        rendered_widgets[widget_instance.id] = rendered_widget

    return rendered_widgets
