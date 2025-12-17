from typing import Callable, Awaitable

from fastapi import Request

from newsflash.widgets.widgets import Widget
from newsflash.templates.templates import template_registry


def build_page_endpoint(
    page: Widget,
    title: str,
) -> Callable[..., Awaitable[str]]:
    async def read_page(request: Request) -> str:
        rendered_content = page.render(request=request)

        page_template = template_registry.get_template("widgets", "index.html")
        return page_template.render(
            request=request,
            title=title,
            content=rendered_content,
        )

    return read_page
