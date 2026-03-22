from typing import (
    Any,
    Mapping,
    Type,
    Callable,
    get_type_hints,
    TypeVar,
    TYPE_CHECKING,
    get_origin,
    Annotated,
)
from inspect import signature
from typing_extensions import Self

from newsflash.svg.element import Element, TemplateParam


if TYPE_CHECKING:
    from newsflash.app import Page


class QueryParam:
    query_param_name: str | None = None

    def __init__(self, query_param_name: str | None = None) -> None:
        self.query_param_name = query_param_name

    def get_query_param_name(self) -> str | None:
        return self.query_param_name


class BodyParam:
    body_param_name: str | None = None

    def __init__(self, body_param_name: str | None = None) -> None:
        self.body_param_name = body_param_name

    def get_body_param_name(self) -> str | None:
        return self.body_param_name


class WidgetContainer(Element):
    widget_id: Annotated[str, TemplateParam()]
    hx_include: Annotated[list[str], TemplateParam()] = []
    template: tuple[str, str] = ("widgets", "container.html")


W = TypeVar("W", bound="Widget")


class Widget(Element):
    hx_include: Annotated[list[str], TemplateParam()] = []
    hx_swap_oob: Annotated[bool, TemplateParam()] = False

    children: list["Widget"] = []
    parent: "Widget | None" = None

    body_params: Mapping[str, str] | None = None

    _include_parent: bool = False
    _callback_fn_name: str | None = None

    def compose(self) -> list["Widget"]:
        return []

    def append_widgets(self) -> list["Widget"]:
        return []

    def model_copy(
        self,
        *,
        copy: bool = False,
        update: Mapping[str, Any] | None = None,
        query_params: Mapping[str, list[str]] | None = None,
        body_params: Mapping[str, Any] | None = None,
        parent: "Widget | None" = None,
    ) -> Self:
        if parent is not None:
            self.parent = parent

        if copy:
            new_instance = super().model_copy(deep=True, update=update)
        else:
            new_instance = self
            if update is not None:
                for k, v in update.items():
                    setattr(new_instance, k, v)

        query_parameters: dict[str, Any] = {}
        body_parameters: dict[str, Any] = {}

        for k, v in new_instance.__class__.model_fields.items():
            if len(v.metadata) == 0:
                continue

            query_param = next(
                (m for m in v.metadata if isinstance(m, QueryParam)), None
            )
            body_param = next((m for m in v.metadata if isinstance(m, BodyParam)), None)

            if query_param is not None and query_params is not None:
                query_param_name = query_param.get_query_param_name() or k
                value_from_request = query_params.get(query_param_name, [])

                if len(value_from_request) == 0:
                    continue

                if get_origin(v.annotation) == list:
                    query_parameters[k] = value_from_request
                else:
                    query_parameters[k] = value_from_request[0]

            elif body_param is not None and body_params is not None:
                body_param_name = body_param.get_body_param_name() or k
                body_param_name = new_instance.id + "-" + body_param_name

                body_value = body_params.get(body_param_name, None)
                if body_value is None:
                    continue

                body_parameters[k] = body_value

        for k, v in query_parameters.items():
            setattr(new_instance, k, v)

        for k, v in body_parameters.items():
            setattr(new_instance, k, v)

        children = new_instance.compose()
        for child in children:
            child.model_copy(
                copy=False,
                query_params=query_params,
                body_params=body_params,
                parent=new_instance,
            )

        new_instance.children = children
        new_instance._build_hx_include()

        return new_instance

    def get_all_children(
        self,
        type: Type[W],
    ) -> list[W]:
        children_of_type = [
            widget.model_copy() for widget in self.children if isinstance(widget, type)
        ]

        if len(self.children) == 0 and isinstance(self, type):
            return []

        for child in self.children:
            child_children = child.get_all_children(
                type=type,
            )

            children_of_type.extend(child_children)

        return children_of_type

    def get_child_widget(
        self,
        type: Type[W],
        id: str | None = None,
    ) -> W:
        children_of_type = [
            widget for widget in self.children if isinstance(widget, type)
        ]

        if id is None:
            all_children_of_type = self.get_all_children(
                type=type,
            )
            if len(all_children_of_type) == 1:
                return all_children_of_type[0]
            else:
                # TODO: distinguish in error message between no or multiple
                # child widgets found.
                raise ValueError(
                    f"Multiple or no widgets of type {type} found. Specify an id."
                )

        id_split = id.split("/")

        if len(id_split) == 1:
            for widget in children_of_type:
                if widget.id == id:
                    widget_copy = widget.model_copy()
                    return widget_copy

        remaining_id = "/".join(id_split[1:])

        for widget in children_of_type:
            if widget.id == id_split[0]:
                widget_copy = widget.model_copy()

                return widget_copy.get_child_widget(
                    type=type,
                    id=remaining_id,
                )

        raise ValueError(f"Widget not found: {type} with id {id}")

    @property
    def full_path(self) -> str:
        if self.parent is not None:
            full_path = f"{self.parent.full_path}/{self.id}"
        else:
            full_path = self.id

        full_path = full_path.strip("/")

        return full_path

    @property
    def root_widget(self) -> "Page":
        if self.parent is None:
            # assert isinstance(self, Page), "Root widget must be a Page"
            # TODO: how to assert the correct type here?
            return self  # type: ignore
        else:
            return self.parent.root_widget

    def get_additional_context(self) -> dict[str, Any]:
        additional_context = super().get_additional_context()

        children_instances = [
            child.model_copy(update={"parent": self}) for child in self.children
        ]
        rendered_children = {child.id: child.render() for child in children_instances}

        additional_context.update({"widgets": rendered_children})
        additional_context.update({"widget_list": list(rendered_children.values())})
        additional_context.update({"full_path": self.full_path})

        return additional_context

    def _build_hx_include(self) -> None:
        callback_fn = self._get_callback_fn()
        if callback_fn is None:
            return

        sig = signature(callback_fn)
        parameters = sig.parameters

        type_hints = get_type_hints(callback_fn)

        include_list: list[str] = []
        for param in parameters:
            if param == "args" or param == "kwargs":
                continue

            widget_type = type_hints[param]
            if not issubclass(widget_type, Widget):
                continue

            include_list.append(f"#{widget_type.model_fields['id'].default}")

        if self._include_parent and self.parent is not None:
            include_list.append(f"#{self.parent.id}")

        self.hx_include = include_list

    def _get_callback_fn(self) -> Callable | None:
        callback_fn_name = self._callback_fn_name
        if callback_fn_name is None:
            return None

        callback_fn = getattr(self, callback_fn_name, None)

        assert callback_fn is not None, (
            f"Widget has no callback function '{callback_fn_name}'"
        )

        return callback_fn

    def _get_callback_inputs(self) -> dict[str, "Widget"]:
        callback_fn = self._get_callback_fn()
        assert callback_fn is not None, "Widget has no callback function"

        sig = signature(callback_fn)
        parameters = sig.parameters

        type_hints = get_type_hints(callback_fn)

        input_dict = {}
        for param in parameters:
            widget_type = type_hints.get(param, "Unknown")
            if widget_type == "Unknown" or not issubclass(widget_type, Widget):
                continue

            widget = self.root_widget.get_child_widget(
                type=widget_type,
            )

            input_dict[param] = widget

        return input_dict

    def _call_callback(self) -> list["Widget"]:
        callback_fn = self._get_callback_fn()
        assert callback_fn is not None, "Widget has no callback function"

        widgets_to_render = callback_fn(**self._get_callback_inputs())
        return widgets_to_render

    def _render_update(self) -> str:
        self.hx_swap_oob = True
        return self.render()
