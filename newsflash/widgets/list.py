from typing import Any, TypeVar, Generic, Self, Callable, Mapping

from .widgets import Widget


W = TypeVar("W", bound=Widget)


class List(Widget, Generic[W]):
    """A widget that displays a list of items."""

    item_type: type[W]
    children: list[W] | None = None
    default: Callable[[], list[W]] | None = None
    template: tuple[str, str] | None = ("widgets", "list.html")

    include_in_context: set[str] = {"id", "hx_include", "hx_swap_oob"}

    def model_copy(self, *, copy: bool = False, update: Mapping[str, Any] | None = None, query_params: Mapping[str, list[str]] | None = None, body_params: Mapping[str, Any] | None = None, parent: Widget | None = None) -> Self:
        new_instance = super().model_copy(copy=copy, update=update, query_params=query_params, body_params=body_params, parent=parent)

        if new_instance.children is None:
            if new_instance.default is not None:
                new_instance.children = new_instance.default()
            else:
                new_instance.children = []

        return new_instance

    def get_list_item_by_id(self, item_id: str) -> W | None:
        if self.children is None:
            return None
        for item in self.children:
            if item.id == item_id:
                return item
        return None

    def get_list_item_by_index(self, index: int) -> W | None:
        if self.children is None:
            return None
        if 0 <= index < len(self.children):
            return self.children[index]
        return None

    @property
    def num_items(self) -> int:
        """Returns the number of items in the list."""
        if self.children is None:
            return 0
        return len(self.children)

    def set_items(self, items: list[W]) -> None:
        self.children = items

    def append_item(self, item: W) -> Self:
        assert self.children is not None, "Items list is not initialized."
        self.children.append(item)
        return self

    def filter_items(self, filter_fn: Callable[[W], bool]) -> Self:
        assert self.children is not None, "Items list is not initialized."
        filtered_items = [item for item in self.children if filter_fn(item)]
        return self.model_copy(update={"items": filtered_items})

    def get_additional_context(self) -> dict[str, Any]:
        assert self.children is not None, "Items list is not initialized."
        for child in self.children:
            child.parent = self

        # TODO: figure out why this assignment complains
        self.children = self.children  # type: ignore

        return super().get_additional_context()

    def get_child_widget(
        self, type: type[W], id: str, body_params: Mapping[str, str] | None = None
    ) -> W:
        child_type = self.item_type
        assert issubclass(child_type, type), (
            f"Child type {child_type} is not a subclass of {type}"
        )

        item_id_split = id.split("/")

        widget_instance = child_type(
            id=item_id_split[0],
            body_params=body_params,
            parent=self,
        )

        if len(item_id_split) == 1:
            return widget_instance
        else:
            return widget_instance.get_child_widget(
                type=type,
                id="/".join(item_id_split[1:]),
            )


class Grid(List[W]):
    """A widget that displays a grid of items."""

    template: tuple[str, str] | None = ("widgets", "grid.html")
    num_columns: int = 2

    include_in_context: set[str] = {"id", "hx_include", "hx_swap_oob", "num_columns"}
