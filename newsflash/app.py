from typing import Type, TypeVar, Mapping
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from newsflash.widgets.widgets import Widget
from newsflash.templates.templates import template_registry
from newsflash.endpoints.callback import get_page_callback, get_callback_endpoint


W = TypeVar("W", bound=Widget)


class Page(Widget):
    path: str
    title: str


class App(FastAPI):
    pages: dict[str, Page]

    def __init__(
        self,
        pages: list[Page],
        template_folders: list[tuple[str, Path]],
        static_folders: list[tuple[str, Path]] = [],
    ) -> None:
        super().__init__(docs_url=None, redoc_url=None, openapi_url=None)

        self.pages = {page.path: page for page in pages}

        for folder in template_folders:
            template_registry.register_template_folder(folder[0], folder[1])

        static_folders.append(
            ("/_newsflash/static", Path(__file__).parent / "assets" / "staticfiles")
        )
        self._mount_static_folders(static_folders)
        self._build_page_endpoints()
        self._build_callback_endpoints()

    def get_widget(
        self,
        path: str,
        type: Type[W],
        id: str | None = None,
        body_params: Mapping[str, str] | None = None,
    ) -> W:
        page = self.pages[path].model_copy(copy=True, body_params=body_params)
        # assert id.startswith(f"{page.id}/"), (
        #     f"Widget id '{id}' not found on page '{page.id}'"
        # )
        if id is not None:
            id = id.removeprefix(f"{page.id}/")

        return page.get_child_widget(type=type, id=id)

    def _mount_static_folders(self, static_folders: list[tuple[str, Path]]) -> None:
        for mount_path, directory in static_folders:
            self.mount(
                mount_path,
                StaticFiles(directory=directory),
            )

    def _build_page_endpoints(self):
        for page_path, page in self.pages.items():
            assert page.template is not None, "Page template is not set."

            page_endpoint = get_page_callback(page)
            self.add_api_route(
                page_path, page_endpoint, methods=["GET"], response_class=HTMLResponse
            )

    def _build_callback_endpoints_for_widget(self, widget: Widget):
        full_path = widget.full_path

        if widget._callback_fn_name is not None:
            print(
                f"Setting up callback endpoint for widget {widget.id} ({widget._callback_fn_name}) at path /{full_path}"
            )
            self.add_api_route(
                f"/{full_path}",
                get_callback_endpoint(widget_id=widget.id, app=self),
                methods=["POST"],
                response_class=HTMLResponse,
            )

        if len(widget.children) > 0:
            for child in widget.children:
                self._build_callback_endpoints_for_widget(child)

    def _build_callback_endpoints(self):
        for page in self.pages.values():
            page.model_copy()
            for child in page.children:
                child.model_copy()
                self._build_callback_endpoints_for_widget(child)
