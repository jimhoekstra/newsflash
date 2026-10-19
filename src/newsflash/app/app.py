from typing import Iterable, Type, Callable
from functools import partial
import secrets

from fastapi import FastAPI, Request, Response, HTTPException, Depends
from fastapi.responses import HTMLResponse
from itsdangerous import TimestampSigner, BadSignature

from newsflash.models import FunctionDefinition, Element
from newsflash.functions import (
    FunctionRegistry,
    get_trigger_context,
    build_function_inputs_from_data,
)
from newsflash.functions import get_trigger_endpoint_url

from .page import Page


class NewsflashApp(FastAPI):
    def __init__(
        self, 
        pages: list[Type[Page]], 
        secret_key: str | None = None,
        max_csrf_cookie_age: int = 3600,
    ) -> None:
        super().__init__(docs_url=None, redoc_url=None)
        if secret_key is None:
            secret_key = secrets.token_urlsafe(32)
        signer = TimestampSigner(secret_key=secret_key)

        self.register_empty_endpoint()
        self.register_page_endpoints(pages=pages, signer=signer, max_csrf_cookie_age=max_csrf_cookie_age)
        self.register_function_endpoints(pages=pages, signer=signer, max_csrf_cookie_age=max_csrf_cookie_age)

    def register_empty_endpoint(self) -> None:
        def empty_request() -> Response:
            return HTMLResponse(content="")

        self.add_api_route(
            path="/_empty",
            endpoint=empty_request,
            methods=["POST"],
        )

    def register_page_endpoints(
        self, 
        pages: list[Type[Page]], 
        signer: TimestampSigner,
        max_csrf_cookie_age: int,
    ) -> None:
        for page in pages:
            # TODO: avoid creating instances of pages here
            page_instance = page()
            self.add_api_route(
                path=page_instance.path,
                endpoint=build_page_endpoint(page=page, signer=signer, max_csrf_cookie_age=max_csrf_cookie_age),
                methods=["GET"],
            )

    def register_function_endpoints(self, pages: list[Type[Page]], signer: TimestampSigner, max_csrf_cookie_age: int) -> None:
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
                    dependencies=[
                        Depends(_require_same_site),
                        Depends(_require_htmx_header),
                        Depends(_build_require_csrf_token_dependency(signer=signer, max_csrf_cookie_age=max_csrf_cookie_age))
                    ]
                )


def build_page_endpoint(page: Type[Page], signer: TimestampSigner, max_csrf_cookie_age: int):

    async def page_endpoint(request: Request) -> Response:
        page_instance = page()
        page_instance.set_fastapi_request_object(request=request)
        
        csrf_token = None
        if cookie := request.cookies.get("csrf_token"):
            try:
                csrf_token = signer.unsign(cookie, max_age=max_csrf_cookie_age).decode()
            except BadSignature:
                csrf_token = secrets.token_urlsafe(32)

        if csrf_token is None:
            csrf_token = secrets.token_urlsafe(32)

        signed_csrf_token = signer.sign(value=csrf_token).decode()
        return page_instance.render(
            request=request, 
            csrf_token=csrf_token, 
            signed_csrf_token=signed_csrf_token,
        )

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


def _require_htmx_header(request: Request) -> None:
    if request.headers.get("HX-Request") != "true":
        raise HTTPException(status_code=401, detail="request not allowed")


def _require_same_site(request: Request) -> None:
    fetch_site = request.headers.get("Sec-Fetch-Site")
    if fetch_site is None or fetch_site != "same-origin":
        raise HTTPException(status_code=401, detail="request not allowed")


def _build_require_csrf_token_dependency(signer: TimestampSigner, max_csrf_cookie_age: int) -> Callable[[Request], None]:
    def _require_csrf_token(request: Request) -> None:
        error_message = "missing or invalid csrf token, try refreshing the page"

        csrf_header = request.headers.get("X-CSRF")
        signed_csrf_cookie = request.cookies.get("csrf_token")

        if csrf_header is None or signed_csrf_cookie is None:
            raise HTTPException(status_code=401, detail=error_message)

        try:
            csrf_cookie = signer.unsign(signed_value=signed_csrf_cookie, max_age=max_csrf_cookie_age).decode()
        except BadSignature:
            raise HTTPException(status_code=401, detail=error_message)

        if not secrets.compare_digest(csrf_cookie, csrf_header):
            raise HTTPException(status_code=401, detail=error_message)

    return _require_csrf_token
