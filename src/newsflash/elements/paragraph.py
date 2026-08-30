from .base import BaseElement


class Paragraph(BaseElement):
    name: str = "paragraph"
    template_dir_name: str = "newsflash-elements"
    template_name: str = "paragraph.html"
    text: str = ""
