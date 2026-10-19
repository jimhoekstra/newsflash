from functools import partial
from typing import Iterable

from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from pydantic import ConfigDict

from newsflash.elements.base import BaseElement
from newsflash.functions import FunctionRegistry, get_trigger_context
from newsflash.templates import template_registry
from newsflash.models import Element


class Page(BaseElement):
    function_registry: FunctionRegistry = FunctionRegistry()
    template_dir_name: str = "newsflash-pages"
    template_name: str = "main.html"
    page_title: str = "newsflash"
    path: str = "/"
    narrow: bool = False

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: str = ""
    name: str = ""

    def render(self, request: Request, csrf_token: str | None, signed_csrf_token: str | None = None) -> Response:
        """Render the newsflash app.

        Parameters
        ----------
        request
            The FastAPI request object.

        Returns
        -------
        A FastAPI response object with an HTML page with the rendered
        newsflash app.
        """
        yielded_elements: Iterable[Element] = []
        for compose_output in self.compose():
            if isinstance(compose_output, Page):
                return RedirectResponse(url=compose_output.path)

            yielded_elements.append(compose_output)

        rendered_elements: dict[str, str] = {}
        for element in yielded_elements:
            _get_trigger_context = partial(
                get_trigger_context,
                functions=self.function_registry,
                page_path=self.path,
            )

            rendered_elements[element.id] = element.render(
                trigger_context_getter=_get_trigger_context,
                hx_swap_oob=None,
            )

        response = template_registry.get_jinja2_templates(
            dir_name=self.template_dir_name,
        ).TemplateResponse(
            request=request,
            name=self.template_name,
            context={
                "elements": rendered_elements,
                "title": self.page_title,
                "narrow": self.narrow,
                "csrf_token": csrf_token,
            },
        )
        if signed_csrf_token is not None:
            response.set_cookie(
                key="csrf_token", 
                value=signed_csrf_token,
                httponly=True,
                samesite="strict",
                # TODO: make max_age configurable
                max_age=3600,
            )
    
        return response
