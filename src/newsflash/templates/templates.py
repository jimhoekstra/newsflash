from pathlib import Path

from jinja2 import Template
from fastapi.templating import Jinja2Templates


class TemplateRegistry:
    _registry: dict[str, Jinja2Templates]

    def __init__(self) -> None:
        self._registry = {}

    def register_template_dir(self, dir_name: str, directory: Path) -> None:
        self._registry[dir_name] = Jinja2Templates(directory=directory)

    def get_jinja2_templates(self, dir_name: str) -> Jinja2Templates:
        return self._registry[dir_name]

    def get_template(self, dir_name: str, template_file_name: str) -> Template:
        templates = self.get_jinja2_templates(dir_name=dir_name)
        return templates.get_template(template_file_name)


template_registry = TemplateRegistry()
template_registry.register_template_dir(
    dir_name="newsflash-elements",
    directory=Path(__file__).resolve().parent / "elements",
)
template_registry.register_template_dir(
    dir_name="newsflash-pages",
    directory=Path(__file__).resolve().parent / "pages",
)
