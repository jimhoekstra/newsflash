from newsflash.svg.element import ElementGroup


class SVG(ElementGroup):
    template: tuple[str, str] = ("svg", "svg.svg")
    width: float
    height: float
    hx_swap_oob: bool = False

    include_in_context: set[str] = {
        "width",
        "height",
        "hx_swap_oob",
        "classes",
        "styles",
        "attributes",
    }
