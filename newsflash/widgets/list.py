from typing import Any, TypeVar, Generic, Self, Callable

from newsflash.endpoints.parsers import RequestValues
from .widgets import Widget


W = TypeVar("W", bound=Widget)


class List(Widget, Generic[W]):
    """A widget that displays a list of items."""

    item_type: type[W]
    items: list[W] | None = None
    default: Callable[[], list[W]] | None = None
    template: tuple[str, str] | None = ("widgets", "list.html")

    include_in_context: set[str] = {"id", "hx_include", "hx_swap_oob"}

    def _post_init(self) -> None:
        if self.items is None:
            if self.default is not None:
                self.items = self.default()
            else:
                self.items = []
        
        super()._post_init()

    def get_list_item_by_id(self, item_id: str) -> W | None:
        if self.items is None:
            return None
        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def get_list_item_by_index(self, index: int) -> W | None:
        if self.items is None:
            return None
        if 0 <= index < len(self.items):
            return self.items[index]
        return None

    @property
    def num_items(self) -> int:
        """Returns the number of items in the list."""
        if self.items is None:
            return 0
        return len(self.items)

    def set_items(self, items: list[W]) -> None:
        self.items = items

    def append_item(self, item: W) -> Self:
        assert self.items is not None, "Items list is not initialized."
        self.items.append(item)
        return self

    def filter_items(self, filter_fn: Callable[[W], bool]) -> Self:
        assert self.items is not None, "Items list is not initialized."
        filtered_items = [item for item in self.items if filter_fn(item)]
        return self.model_copy(update={"items": filtered_items})

    def get_additional_context(self) -> dict[str, Any]:
        assert self.items is not None, "Items list is not initialized."
        for child in self.items:
            child.parent = self

        # TODO: figure out why this assignment complains
        self.children = self.items  # type: ignore

        return super().get_additional_context()

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

    def get_child_widget(
        self, type: type[W], id: str, request_values: RequestValues | None = None
    ) -> W:
        child_type = self.item_type
        assert issubclass(child_type, type), (
            f"Child type {child_type} is not a subclass of {type}"
        )

        item_id_split = id.split("/")

        widget_instance = child_type(
            id=item_id_split[0],
            request_values=request_values,
            parent=self,
        )
        widget_instance._post_init()

        if len(item_id_split) == 1:
            return widget_instance
        else:
            return widget_instance.get_child_widget(
                type=type,
                id="/".join(item_id_split[1:]),
                request_values=request_values,
            )


class Grid(List[W]):
    """A widget that displays a grid of items."""

    template: tuple[str, str] | None = ("widgets", "grid.html")
    num_columns: int = 2

    include_in_context: set[str] = {"id", "hx_include", "hx_swap_oob", "num_columns"}
