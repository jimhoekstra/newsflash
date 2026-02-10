from typing import TYPE_CHECKING

from fastapi import Request
from newsflash.templates.templates import template_registry

if TYPE_CHECKING:
    from newsflash.app import Page


def get_page_callback(page: "Page"):
    async def page_endpoint(request: Request) -> str:
        query_params = request.query_params
        query_params_dict: dict[str, list[str]] = {}
        for k in query_params.keys():
            query_params_dict[k] = query_params.getlist(k)

        page_copy = page.model_copy(deep=True)

        page_attrs = page_copy.__class__.__annotations__
        for k, vs in query_params_dict.items():
            # TODO
            # It doesn't make much sense to loop through all values in this case,
            # because only the last value will be used.
            for v in vs:
                if k in page_attrs:
                    attr_type = page_attrs[k]
                    setattr(page_copy, k, attr_type(v))

        page_copy._post_init()
        page_copy.query_params = query_params_dict

        for child in page_copy.children:
            child._post_init()

        rendered_content = page_copy.render()

        page_template = template_registry.get_template("widgets", "index.html")
        return page_template.render(
            request=request,
            title=page_copy.title,
            content=rendered_content,
        )

    return page_endpoint
