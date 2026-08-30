from typing import Iterable, Any
from functools import partial

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from starlette.datastructures import FormData
from pydantic import ValidationError

from newsflash.elements import Element
from newsflash.functions import FunctionRegistry, FunctionDefinition, get_trigger_context
from newsflash.templates import template_registry


def collect_function_inputs(
    fn: FunctionDefinition, values: FormData
) -> dict[str, Element | None]:
    function_inputs: dict[str, Element | None] = {}

    for function_input in fn.inputs:
        input_type = function_input.element_type

        input_values: dict[str, Any] = {
            "id": function_input.element_id,
        }

        for k, v in values.items():
            input_id, input_parameter = k.split("--")
            if input_id == function_input.element_id:
                input_values[input_parameter] = v

        try:
            input_element = input_type.model_validate(input_values)
            function_inputs[function_input.arg_name] = input_element
        except ValidationError:
            function_inputs[function_input.arg_name] = None
            # TODO: display validation error in the UI at the element's position
            print(f"Failed to parse input values for: {function_input.element_id}")

    return function_inputs


def build_function_endpoint(
    fns: list[FunctionDefinition], fn_registry: FunctionRegistry
):

    _get_trigger_context = partial(
        get_trigger_context,
        functions=fn_registry,
    )

    async def function_endpoint(request: Request) -> HTMLResponse:
        body = await request.form()
        collected_outputs: Iterable[Element] = []

        for fn in fns:
            fn_inputs = collect_function_inputs(
                fn=fn,
                values=body,
            )

            if any([fn_input is None for fn_input in fn_inputs.values()]):
                # TODO: handle with a message showing up in the UI
                print(
                    f"Failed to call function: {fn.func.__name__} because of missing inputs"
                )
                continue

            fn_outputs: Iterable[Element] = fn.func(**fn_inputs)
            collected_outputs.extend(fn_outputs)

        rendered_outputs: list[str] = []
        for fn_output in collected_outputs:

            rendered_outputs.append(fn_output.render(
                trigger_context_getter=_get_trigger_context,
                hx_swap_oob="true",
            ))

        return HTMLResponse(content="\n".join(rendered_outputs), status_code=200)

    return function_endpoint


class NewsflashApp(FastAPI):
    function_registry: FunctionRegistry
    template_dir_name: str = "newsflash-pages"
    template_name: str = "main.html"
    page_title: str = "newsflash"

    def __init__(self, functions: FunctionRegistry) -> None:
        super().__init__()
        self.function_registry = functions
        self.register_root_page()
        self.register_function_endpoints()

    def register_root_page(self) -> None:
        def root_page(request: Request) -> Response:
            return self.render(request=request)

        self.add_api_route(path="/", endpoint=root_page, methods=["GET"])

    def register_function_endpoints(self) -> None:

        element_to_fn_definitions = _build_element_to_fn_definitions_map(
            function_definitions=self.function_registry.functions
        )

        for (
            trigger_name,
            trigger_id,
            trigger_event,
        ), fn_definitions in element_to_fn_definitions.items():
            self.add_api_route(
                path=f"/{trigger_name}/{trigger_id}/{trigger_event}",
                endpoint=build_function_endpoint(
                    fns=fn_definitions, fn_registry=self.function_registry
                ),
                methods=["POST"],
            )

    def render(self, request: Request) -> Response:
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
        yield from ()


def _build_element_to_fn_definitions_map(
    function_definitions: list[FunctionDefinition],
) -> dict[tuple[str, str, str], list[FunctionDefinition]]:
    element_to_fn_definitions: dict[tuple[str, str, str], list[FunctionDefinition]] = {}

    for fn_definition in function_definitions:
        for trigger in fn_definition.triggers:
            if (
                trigger.element_name,
                trigger.element_id,
                trigger.trigger,
            ) not in element_to_fn_definitions:
                element_to_fn_definitions[
                    (trigger.element_name, trigger.element_id, trigger.trigger)
                ] = [fn_definition]
            else:
                element_to_fn_definitions[
                    (trigger.element_name, trigger.element_id, trigger.trigger)
                ].append(fn_definition)

    return element_to_fn_definitions
