from typing import Any, TypeVar, Generic, Self, Callable

from newsflash.endpoints.parsers import RequestValues
from .widgets import Widget


W = TypeVar("W", bound=Widget)

class List(Widget, Generic[W]):
    """A widget that displays a list of items."""

    item_type: type[W]
    items: list[W] = []
    template: tuple[str, str] | None = ("widgets", "list.html")

    def get_list_item_by_id(self, item_id: str) -> W | None:
        """Gets a list item by its ID.

        Parameters
        ----------
        item_id
            The ID of the list item to retrieve.

        Returns
        -------
        The list item with the specified ID, or None if not found.
        """
        for item in self.items:
            if item.id == item_id:
                return item
        return None
    
    def get_list_item_by_index(self, index: int) -> W | None:
        """Gets a list item by its index.

        Parameters
        ----------
        index
            The index of the list item to retrieve.

        Returns
        -------
        The list item at the specified index, or None if index is out of range.
        """
        if 0 <= index < len(self.items):
            return self.items[index]
        return None
    
    @property
    def num_items(self) -> int:
        """Returns the number of items in the list."""
        return len(self.items)
 
    def set_items(self, items: list[W]) -> Self:
        self.items = items

    def append_item(self, item: W) -> Self:
        self.items.append(item)
        return self
    
    def filter_items(self, filter_fn: Callable[[W], bool]) -> Self:
        filtered_items = [item for item in self.items if filter_fn(item)]
        return self.model_copy(update={"items": filtered_items})

    def get_additional_context(self) -> dict[str, Any]:
        """Returns additional context for rendering the widget.

        Returns
        -------
        A dictionary containing the additional context.
        """
        additional_context = super().get_additional_context()

        rendered_children = {child.id: child.render() for child in self.items}

        additional_context.update({"widgets": rendered_children})
        additional_context.update({"full_path": self.full_path})

        return additional_context
    
    def _set_values_from_request(self, inputs: RequestValues) -> None:
        super()._set_values_from_request(inputs)
        items: list[W] = []

        item_idx = 0
        while f"{self.id}-{item_idx}-id" in inputs.widget_attributes:
            item_id = inputs.widget_attributes[f"{self.id}-{item_idx}-id"]

            item_widget = self.item_type(
                id=item_id,
                request_values=inputs,
                parent=self,
            )
            item_widget._post_init()
            
            items.append(item_widget)
            item_idx += 1

        self.items = items
