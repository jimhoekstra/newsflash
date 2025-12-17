from typing import Type, TypeVar
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from newsflash.widgets.widgets import Widget
from newsflash.widgets import Notifications
from newsflash.templates.templates import template_registry
from newsflash.endpoints.page import build_page_endpoint
from newsflash.endpoints.callback import build_callback_endpoint


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
    ) -> None:
        super().__init__()

        self.pages = {page.path: page for page in pages}

        for folder in template_folders:
            template_registry.register_template_folder(folder[0], folder[1])

        self._build_page_endpoints()
        self._build_callback_endpoints()

    def query_one(self, path: str, type: Type[W], id: str | None = None) -> Type[W]:
        page = self.pages[path]
        widgets_of_type = [
            widget for widget in page.children if issubclass(widget, type)
        ]

        if id is None:
            if len(widgets_of_type) == 1:
                return widgets_of_type[0]
            elif len(widgets_of_type) > 1:
                raise ValueError(
                    f"Multiple widgets of type {type} found on page {path}, "
                    f"please specify an id"
                )
        else:
            for widget in widgets_of_type:
                if widget().id == id:
                    return widget

        raise ValueError(f"Widget not found: {type} with id {id} on page {path}")

    def _build_page_endpoints(self):
        newsflash_static_dir = (
            Path(__file__).resolve().parent / "assets" / "staticfiles"
        )
        self.mount(
            "/static", StaticFiles(directory=newsflash_static_dir), name="static"
        )

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
            "/_newsflash/{widget_id}",
            callback_endpoint,
            methods=["POST"],
            response_class=HTMLResponse,
        )
