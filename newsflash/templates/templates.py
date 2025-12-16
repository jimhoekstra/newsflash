from pathlib import Path

from jinja2 import Template
from fastapi.templating import Jinja2Templates


ROOT_TEMPLATE_DIR = Path(__file__).parent

_template_registry: dict[str, Jinja2Templates] = {
    "widgets": Jinja2Templates(directory=ROOT_TEMPLATE_DIR / "widgets"),
    "svg": Jinja2Templates(directory=ROOT_TEMPLATE_DIR / "svg"),
}

def get_template(template_folder: str, template_name: str) -> Template:
    templates = _template_registry[template_folder]
    return templates.get_template(template_name)
