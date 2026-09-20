from .base import BaseElement


class Link(BaseElement):
    name: str = "link"
    template_dir_name: str = "newsflash-elements"
    template_name: str = "link.html"

    href: str
    text: str
