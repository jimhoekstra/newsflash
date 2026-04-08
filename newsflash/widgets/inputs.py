from typing import Any, Callable, Annotated, Mapping, Self

from newsflash.svg.element import TemplateParam
from .widgets import Widget, BodyParam


class Input(Widget):
    template: tuple[str, str] = ("widgets", "input.html")
    value: Annotated[str | None, BodyParam(), TemplateParam()] = None
    default: Callable[[], str] | None = None
    autofocus: Annotated[bool, TemplateParam()] = False
    type: Annotated[str, TemplateParam()] = "text"
    placeholder: Annotated[str, TemplateParam()] = ""

    _callback_fn_name: str = "on_input"

    def initialize(
        self,
        *,
        copy: bool = False,
        update: Mapping[str, Any] | None = None,
        query_params: Mapping[str, list[str]] | None = None,
        body_params: Mapping[str, Any] | None = None,
        parent: Widget | None = None,
    ) -> Self:
        new_instance = super().initialize(
            copy=copy,
            update=update,
            query_params=query_params,
            body_params=body_params,
            parent=parent,
        )
        if new_instance.value is None:
            if new_instance.default is not None:
                new_instance.value = new_instance.default()
            else:
                new_instance.value = ""

        return new_instance

    def on_input(self, *args, **kwargs) -> list[Widget]:
        """Event handler for input events."""
        return []


class TextArea(Input):
    template: tuple[str, str] = ("widgets", "textarea.html")
    rows: Annotated[int, TemplateParam()] = 7
    spellcheck: Annotated[bool, TemplateParam()] = False


class Select(Widget):
    template: tuple[str, str] = ("widgets", "select.html")
    options: Annotated[list[str], TemplateParam()] = ["-"]
    selected: Annotated[str | None, BodyParam(), TemplateParam()] = None
    default: Callable[[], str] | None = None

    _callback_fn_name: str = "on_select"

    def initialize(
        self,
        *,
        copy: bool = False,
        update: Mapping[str, Any] | None = None,
        query_params: Mapping[str, list[str]] | None = None,
        body_params: Mapping[str, Any] | None = None,
        parent: Widget | None = None,
    ) -> Self:
        new_instance = super().initialize(
            copy=copy,
            update=update,
            query_params=query_params,
            body_params=body_params,
            parent=parent,
        )

        if new_instance.selected is None:
            if new_instance.default is not None:
                new_instance.selected = new_instance.default()
            elif len(new_instance.options) > 0:
                new_instance.selected = new_instance.options[0]
            else:
                raise ValueError("Select widget has no options to select from.")

        return new_instance

    def on_select(self, *args, **kwargs) -> list[Widget]:
        """Event handler for select events."""
        return []


class Button(Widget):
    template: tuple[str, str] = ("widgets", "button.html")
    label: Annotated[str, TemplateParam()] = "Click Me"
    disabled: Annotated[bool, TemplateParam()] = False
    classes: Annotated[list[str], TemplateParam()] = ["newsflash-button"]

    _callback_fn_name: str = "on_click"

    def on_click(self, *args, **kwargs) -> list[Widget]:
        """Event handler for button click events."""
        return []
