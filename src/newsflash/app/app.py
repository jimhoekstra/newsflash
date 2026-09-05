from typing import Iterable
from functools import partial

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse

from newsflash.models import FunctionDefinition, Element
from newsflash.functions import (
    FunctionRegistry,
    get_trigger_context,
    build_function_inputs_from_data,
)
from newsflash.templates import template_registry


class NewsflashApp(FastAPI):
    function_registry: FunctionRegistry
    template_dir_name: str = "newsflash-pages"
    template_name: str = "main.html"
    page_title: str = "newsflash"

    def __init__(self, functions: FunctionRegistry) -> None:
        super().__init__()
        self.function_registry = functions
        # TODO: allow for registering multiple pages at different
        # paths
        self.register_root_page()
        self.register_empty_endpoint()
        self.register_function_endpoints()

    def register_root_page(self) -> None:
        def root_page(request: Request) -> Response:
            return self.render(request=request)

        self.add_api_route(path="/", endpoint=root_page, methods=["GET"])

    def register_empty_endpoint(self) -> None:
        def empty_request() -> Response:
            return HTMLResponse(content="")

        self.add_api_route(
            path="/_empty",
            endpoint=empty_request,
            methods=["GET"],
        )

    def register_function_endpoints(self) -> None:
        element_to_fn_definitions = _build_element_to_function_definitions_map(
            function_definitions=self.function_registry._functions
        )

        for trigger_path, fn_definitions in element_to_fn_definitions.items():
            self.add_api_route(
                path=trigger_path,
                endpoint=build_function_endpoint(
                    function_definitions=fn_definitions,
                    function_registry=self.function_registry,
                ),
                methods=["POST"],
            )

    def render(self, request: Request) -> Response:
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
                functions=self.function_registry,
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

    def compose(self) -> Iterable["Element"]:
        """Compose the app, empty until overwritten."""
        yield from ()


def build_function_endpoint(
    function_definitions: list[FunctionDefinition], function_registry: FunctionRegistry
):

    _get_trigger_context = partial(
        get_trigger_context,
        functions=function_registry,
    )

    # TODO: dynamically set the parameters of this function if there are
    # "Depends" injections required for the FastAPI endpoint as configured
    # by the library users in the callback function signatures.
    async def function_endpoint(request: Request) -> HTMLResponse:
        body = await request.form()
        collected_outputs: Iterable[Element] = []

        for function_definition in function_definitions:
            function_inputs = build_function_inputs_from_data(
                function_definition=function_definition,
                values={k: v for k, v in body.items() if isinstance(v, str)},
            )

            if any([fn_input is None for fn_input in function_inputs.values()]):
                # TODO: handle with a message showing up in the UI
                print(
                    f"Failed to call function: {function_definition.func.__name__} because of missing inputs"
                )
                continue

            fn_outputs: Iterable[Element] = function_definition.func(**function_inputs)
            collected_outputs.extend(fn_outputs)

        rendered_outputs: list[str] = []
        for fn_output in collected_outputs:
            rendered_outputs.append(
                fn_output.render(
                    trigger_context_getter=_get_trigger_context,
                    hx_swap_oob="true",
                )
            )

        return HTMLResponse(content="\n".join(rendered_outputs), status_code=200)

    return function_endpoint


def _build_element_to_function_definitions_map(
    function_definitions: list[FunctionDefinition],
) -> dict[str, list[FunctionDefinition]]:
    element_to_fn_definitions: dict[str, list[FunctionDefinition]] = {}

    for fn_definition in function_definitions:
        for trigger in fn_definition.triggers:
            trigger_path = trigger.to_path()
            if trigger_path not in element_to_fn_definitions:
                element_to_fn_definitions[trigger_path] = [fn_definition]
            else:
                element_to_fn_definitions[trigger_path].append(fn_definition)

    return element_to_fn_definitions
