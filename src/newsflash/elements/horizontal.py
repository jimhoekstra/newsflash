from .base import BaseElement


class Horizontal(BaseElement):
    name: str = "horizontal"
    template_dir_name: str = "newsflash-elements"
    template_name: str = "horizontal.html"

    wide: bool = False
