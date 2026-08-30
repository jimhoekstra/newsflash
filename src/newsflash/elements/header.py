from .base import BaseElement


class Header(BaseElement):
    name: str = "header"
    template_dir_name: str = "newsflash-elements"
    template_name: str = "header.html"
    level: int = 1
    text: str = ""
