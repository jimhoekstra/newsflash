from pathlib import Path

from jinja2 import Template
from fastapi.templating import Jinja2Templates


ROOT_TEMPLATE_DIR = Path(__file__).parent


class TemplateRegistry:
    def __init__(self) -> None:
        self._registry: dict[str, Jinja2Templates] = {}

    def register_template_folder(self, folder_name: str, directory: Path) -> None:
        self._registry[folder_name] = Jinja2Templates(directory=directory)

    def get_template(self, template_folder: str, template_name: str) -> Template:
        templates = self._registry[template_folder]
        return templates.get_template(template_name)


template_registry = TemplateRegistry()
template_registry.register_template_folder("widgets", ROOT_TEMPLATE_DIR / "widgets")
template_registry.register_template_folder("svg", ROOT_TEMPLATE_DIR / "svg")
