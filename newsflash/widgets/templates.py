from pathlib import Path
from fastapi.templating import Jinja2Templates


widget_templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
