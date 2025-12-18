from typing import Type, TypeVar
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from newsflash.widgets.widgets import Widget
from newsflash.widgets import Notifications
from newsflash.templates.templates import template_registry
from newsflash.endpoints.page import build_page_endpoint
from newsflash.endpoints.callback import build_callback_endpoint
from newsflash.endpoints.parsers import RequestValues


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
        super().__init__()

        self.pages = {page.path: page for page in pages}

        for folder in template_folders:
            template_registry.register_template_folder(folder[0], folder[1])

        static_folders.append(
            ("/_newsflash/static", Path(__file__).parent / "assets" / "staticfiles")
        )
        self._mount_static_folders(static_folders)

        self._build_page_endpoints()
        self._build_callback_endpoints()

    def query_one(
        self,
        path: str,
        type: Type[W],
        id: str,
        request_values: RequestValues | None = None,
    ) -> W:
        page = self.pages[path]
        id = id.removeprefix(f"{page.id}/")
        return page.get_child_widget(type=type, id=id, request_values=request_values)

    def _mount_static_folders(self, static_folders: list[tuple[str, Path]]) -> None:
        for mount_path, directory in static_folders:
            self.mount(
                mount_path,
                StaticFiles(directory=directory),
            )

    def _build_page_endpoints(self):
        for page_path, page in self.pages.items():
            assert page.template is not None, "Page template is not set."

            page.children.append(Notifications)  # Automatically add Notification widget

            page_endpoint = build_page_endpoint(
                page=page,
                title=page.title,
            )
            self.add_api_route(
                page_path, page_endpoint, methods=["GET"], response_class=HTMLResponse
            )

    def _build_callback_endpoints(self):
        callback_endpoint = build_callback_endpoint(self)

        self.add_api_route(
            "/{widget_id:path}",
            callback_endpoint,
            methods=["POST"],
            response_class=HTMLResponse,
        )
