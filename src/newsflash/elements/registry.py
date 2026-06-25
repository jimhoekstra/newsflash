import typing

from .base import Element

ElementT = typing.TypeVar("ElementT", bound=typing.Type[Element])


class ElementRegistry:
    elements: list[Element]

    def __init__(self) -> None:
        self.elements = []

    def add(self, ids: list[str]):

        def decorator(cls: ElementT) -> ElementT:
            for element_id in ids:
                self.elements.append(cls(id=element_id))  # type: ignore

            return cls

        return decorator
