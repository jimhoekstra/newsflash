from typing import Type, TypeVar
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from newsflash.widgets.widgets import Widget
from newsflash.widgets.card import CompositeWidget
from newsflash.widgets import Notifications
from newsflash.endpoints.page import build_page_endpoint
from newsflash.endpoints.callback import build_callback_endpoint


W = TypeVar("W", bound=Widget)


class Page(BaseModel):
    path: str
    title: str
    template: str
    widgets: list[Type[Widget]]


class App(FastAPI):
    pages: dict[str, Page]
    template_dir: Path

    def __init__(
        self,
        pages: list[Page],
        template_dir: Path = Path.cwd() / "templates",
    ) -> None:
        super().__init__()

        self.pages = {page.path: page for page in pages}
        self.template_dir = template_dir

        self._add_child_widgets()
        self._build_page_endpoints()
        self._build_callback_endpoints()

    def _add_child_widgets(self):
        for page in self.pages.values():
            all_widgets: list[Type[Widget]] = []

            for widget in page.widgets:
                all_widgets.append(widget)

                if issubclass(widget, CompositeWidget):
                    composite_instance = widget()
                    child_widgets = composite_instance.get_components()
                    all_widgets.extend(child_widgets)

            page.widgets = all_widgets

    def query_one(self, path: str, type: Type[W], id: str | None = None) -> Type[W]:
        page = self.pages[path]
        widgets_of_type = [
            widget for widget in page.widgets if issubclass(widget, type)
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
        templates = Jinja2Templates(directory=self.template_dir)

        for page_path, page in self.pages.items():
            page.widgets.append(Notifications)  # Automatically add Notification widget

            page_endpoint = build_page_endpoint(
                page_title=page.title,
                page_template_name=page.template,
                widgets=page.widgets,
                templates=templates,
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
