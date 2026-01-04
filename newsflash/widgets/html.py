from .widgets import Widget


class HTML(Widget):
    template: tuple[str, str] = ("widgets", "html.html")
    html_content: str = ""

    _values_from_request: set[str] = {
        "html_content",
    }

    include_in_context: set[str] = {
        "id",
        "hx_swap_oob",
        "html_content",
    }
