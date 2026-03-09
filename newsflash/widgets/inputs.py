from typing import Any, Callable, Annotated, Mapping, Self

from .widgets import Widget, BodyParam


class Input(Widget):
    template: tuple[str, str] = ("widgets", "input.html")
    value: Annotated[str | None, BodyParam()] = None
    default: Callable[[], str] | None = None
    autofocus: bool = False
    type: str = "text"
    placeholder: str = ""

    include_in_context: set[str] = {
        "id",
        "value",
        "hx_include",
        "hx_swap_oob",
        "full_path",
        "autofocus",
        "type",
        "placeholder",
    }

    _values_from_request: list[str] = ["value"]
    _callback_fn_name: str = "on_input"

    def model_copy(
        self,
        *,
        copy: bool = False,
        update: Mapping[str, Any] | None = None,
        query_params: Mapping[str, list[str]] | None = None,
        body_params: Mapping[str, Any] | None = None,
        parent: Widget | None = None,
    ) -> Self:
        new_instance = super().model_copy(
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
    rows: int = 7
    spellcheck: bool = False

    include_in_context: set[str] = {
        "id",
        "hx_include",
        "hx_swap_oob",
        "full_path",
        "autofocus",
        "value",
        "rows",
        "spellcheck",
        "placeholder",
    }


class Select(Widget):
    template: tuple[str, str] = ("widgets", "select.html")
    options: list[str] = ["-"]
    selected: Annotated[str | None, BodyParam()] = None
    default: Callable[[], str] | None = None

    include_in_context: set[str] = {
        "id",
        "hx_include",
        "hx_swap_oob",
        "full_path",
        "options",
        "selected",
    }

    _callback_fn_name: str = "on_select"
    _values_from_request: list[str] = ["selected"]

    def model_copy(
        self,
        *,
        copy: bool = False,
        update: Mapping[str, Any] | None = None,
        query_params: Mapping[str, list[str]] | None = None,
        body_params: Mapping[str, Any] | None = None,
        parent: Widget | None = None,
    ) -> Self:
        new_instance = super().model_copy(
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
    label: str = "Click Me"
    hx_include: list[str] = []
    disabled: bool = False
    classes: list[str] = ["newsflash-button"]

    include_in_context: set[str] = {
        "id",
        "hx_include",
        "hx_swap_oob",
        "full_path",
        "label",
        "disabled",
        "classes",
    }

    _callback_fn_name: str = "on_click"

    def on_click(self, *args, **kwargs) -> list[Widget]:
        """Event handler for button click events."""
        return []
