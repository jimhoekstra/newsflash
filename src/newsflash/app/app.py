from typing import Iterable, Type
from functools import partial

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse

from newsflash.models import FunctionDefinition, Element
from newsflash.functions import (
    FunctionRegistry,
    get_trigger_context,
    build_function_inputs_from_data,
)
from newsflash.functions import get_trigger_endpoint_url

from .page import Page


class NewsflashApp(FastAPI):
    def __init__(self, pages: list[Type[Page]]) -> None:
        super().__init__()
        self.register_empty_endpoint()
        self.register_page_endpoints(pages=pages)
        self.register_function_endpoints(pages=pages)

    def register_empty_endpoint(self) -> None:
        def empty_request() -> Response:
            return HTMLResponse(content="")

        self.add_api_route(
            path="/_empty",
            endpoint=empty_request,
            methods=["POST"],
        )

    def register_page_endpoints(self, pages: list[Type[Page]]) -> None:
        for page in pages:
            # TODO: avoid creating instances of pages here
            page_instance = page()
            self.add_api_route(
                path=page_instance.path,
                endpoint=build_page_endpoint(page=page),
                methods=["GET"],
            )

    def register_function_endpoints(self, pages: list[Type[Page]]) -> None:
        for page in pages:
            page_instance = page()

            element_to_fn_definitions = _build_element_to_function_definitions_map(
                page_path=page_instance.path,
                function_definitions=page_instance.function_registry._functions,
            )

            for trigger_path, fn_definitions in element_to_fn_definitions.items():
                function_endpoint = build_function_endpoint(
                    page_path=page_instance.path,
                    function_definitions=fn_definitions,
                    function_registry=page_instance.function_registry,
                )

                self.add_api_route(
                    path=trigger_path,
                    endpoint=function_endpoint,
                    methods=["POST"],
                )


def build_page_endpoint(page: Type[Page]):

    async def page_endpoint(request: Request) -> Response:
        page_instance = page()
        page_instance.set_fastapi_request_object(request=request)
        return page_instance.render(request=request)

    return page_endpoint


def build_function_endpoint(
    page_path: str,
    function_definitions: list[FunctionDefinition],
    function_registry: FunctionRegistry,
):

    _get_trigger_context = partial(
        get_trigger_context,
        functions=function_registry,
        page_path=page_path,
    )

    # TODO: dynamically set the parameters of this function if there are
    # "Depends" injections required for the FastAPI endpoint as configured
    # by the library users in the callback function signatures.
    async def function_endpoint(request: Request, response: Response) -> Response:
        body = await request.form()
        collected_outputs: dict[str, Element] = {}

        for function_definition in function_definitions:
            function_inputs = build_function_inputs_from_data(
                function_definition=function_definition,
                values={k: v for k, v in body.items() if isinstance(v, str)},
                request=request,
                response=response,
            )

            if any([fn_input is None for fn_input in function_inputs.values()]):
                # TODO: handle with a message showing up in the UI
                print(
                    f"Failed to call function: {function_definition.func.__name__} because of missing inputs"
                )
                continue

            yielded_elements: Iterable[Element] = []
            for function_output in function_definition.func(**function_inputs):
                if isinstance(function_output, Page):
                    return Response(headers={"HX-Redirect": function_output.path})

                yielded_elements.append(function_output)
            
            for function_output in yielded_elements:
                # If the same element (based on ID) is returned multiple times (
                # by different functions or even within one function), then we only
                # keep the last one. #TODO: raise explicit warning to user if this
                # happens.
                collected_outputs[function_output.id] = function_output

        rendered_outputs: list[str] = []
        for function_output in collected_outputs.values():
            rendered_outputs.append(
                function_output.render(
                    trigger_context_getter=_get_trigger_context,
                    hx_swap_oob="true",
                )
            )

        return HTMLResponse(
            content="\n".join(rendered_outputs), 
            status_code=200,
        )

    return function_endpoint


def _build_element_to_function_definitions_map(
    page_path: str,
    function_definitions: list[FunctionDefinition],
) -> dict[str, list[FunctionDefinition]]:
    element_to_fn_definitions: dict[str, list[FunctionDefinition]] = {}

    for fn_definition in function_definitions:
        for trigger in fn_definition.triggers:
            trigger_path = get_trigger_endpoint_url(
                trigger=trigger, page_path=page_path
            )

            if trigger_path not in element_to_fn_definitions:
                element_to_fn_definitions[trigger_path] = [fn_definition]
            else:
                element_to_fn_definitions[trigger_path].append(fn_definition)

    return element_to_fn_definitions
