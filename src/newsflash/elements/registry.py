import typing

from .base import BaseElement

ElementT = typing.TypeVar("ElementT", bound=typing.Type[BaseElement])


class ElementRegistry:
    elements: list[BaseElement]

    def __init__(self) -> None:
        self.elements = []

    def add(self, ids: list[str]):

        def decorator(cls: ElementT) -> ElementT:
            for element_id in ids:
                self.elements.append(cls(id=element_id))  # type: ignore

            return cls

        return decorator
