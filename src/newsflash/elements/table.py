from typing import Any, TypeVar, Generic

from pydantic import BaseModel

from .base import BaseElement

M = TypeVar("M", bound=BaseModel)


class Table(BaseElement, Generic[M]):
    name: str = "table"
    template_dir_name: str = "newsflash-elements"
    template_name: str = "table.html"

    data: list[M]

    def _build_additional_context(self) -> dict[str, Any]:
        if len(self.data) == 0:
            return {}
        
        headers = list(self.data[0].__class__.model_fields.keys())
        rows = [
            [getattr(item, header) for header in headers] for item in self.data
        ]

        return {
            "headers": headers,
            "rows": rows,
        }
