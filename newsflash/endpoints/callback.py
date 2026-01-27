from typing import TYPE_CHECKING

from fastapi import Request
from newsflash.templates.templates import template_registry

if TYPE_CHECKING:
    from newsflash.app import Page


def get_page_callback(page: "Page"):
    async def page_endpoint(request: Request) -> str:
        page_copy = page.model_copy(deep=True)
        page_copy._re_init()
        for child in page_copy.children:
            child._re_init()

        rendered_content = page_copy.render()

        page_template = template_registry.get_template("widgets", "index.html")
        return page_template.render(
            request=request,
            title=page_copy.title,
            content=rendered_content,
        )

    return page_endpoint
