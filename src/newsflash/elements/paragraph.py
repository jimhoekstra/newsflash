from .base import Element


class Paragraph(Element):
    name: str = "paragraph"
    template_dir_name: str = "newsflash-elements"
    template_name: str = "paragraph.html"
    text: str = ""
