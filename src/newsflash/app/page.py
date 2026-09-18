from functools import partial

from fastapi import Request
from fastapi.responses import HTMLResponse
from pydantic import ConfigDict

from newsflash.elements.base import BaseElement
from newsflash.functions import FunctionRegistry, get_trigger_context
from newsflash.templates import template_registry
from newsflash.models import Element


class Page(BaseElement):
    function_registries: list[FunctionRegistry]
    template_dir_name: str = "newsflash-pages"
    template_name: str = "main.html"
    page_title: str = "newsflash"
    path: str = "/"

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: str = ""
    name: str = ""

    def render(self, request: Request) -> HTMLResponse:
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
        elements = list(self.compose())

        rendered_elements: dict[str, str] = {}
        for element in elements:
            _get_trigger_context = partial(
                get_trigger_context,
                functions=self.combined_function_registry,
            )

            rendered_elements[element.id] = element.render(
                trigger_context_getter=_get_trigger_context,
                hx_swap_oob=None,
            )

        return template_registry.get_jinja2_templates(
            dir_name=self.template_dir_name,
        ).TemplateResponse(
            request=request,
            name=self.template_name,
            context={
                "elements": rendered_elements,
                "title": self.page_title,
            },
        )

    @property
    def combined_function_registry(self) -> FunctionRegistry:
        combined_function_registry = self._build_default_functions()
        for function_registry in self.function_registries:
            combined_function_registry = combined_function_registry.combine_with(other=function_registry)

        return combined_function_registry

    def _build_default_functions(self) -> FunctionRegistry:
        default_function_registry = FunctionRegistry()
        all_children: list[Element] = []

        for child in self.compose():
            all_children.append(child)
            all_children.extend(child._get_all_children())

        for child in all_children:
            for default_function in child._get_default_functions():
                default_function_registry._append_function(
                    function_definition=default_function,
                )

        return default_function_registry
