from pathlib import Path
from fastapi.templating import Jinja2Templates


svg_templates = Jinja2Templates(directory=Path(__file__).parent)
