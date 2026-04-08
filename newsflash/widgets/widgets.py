from typing import (
    Annotated,
    Any,
    Callable,
    get_type_hints,
    get_origin,
    Mapping,
    Type,
    TypeVar,
    TYPE_CHECKING,
)
from inspect import signature
from typing_extensions import Self

from newsflash.svg.element import Element, TemplateParam

# Avoid circular import by only importing Page for type checking.
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

    def compose(self) -> list["Widget"]:
        return []

    def append_widgets(self) -> list["Widget"]:
        return []

    def initialize(
        self,
        *,
        copy: bool = False,
        update: Mapping[str, Any] | None = None,
        query_params: Mapping[str, list[str]] | None = None,
        body_params: Mapping[str, Any] | None = None,
        parent: "Widget | None" = None,
    ) -> Self:
        """
        Hydrate this widget with request data and recursively build the child tree.

        This method sits at the heart of the request-response cycle:

        **Page requests (GET)**
            The framework calls ``page.initialize(copy=True, query_params=...)`` on the
            root ``Page`` widget. Fields annotated with ``QueryParam`` are populated from
            the URL query string. ``compose()`` is then called to produce child widgets,
            and ``initialize`` recurses into each child so the entire tree is hydrated
            before ``render()`` is called to produce the HTML response.

        **Callback requests (POST / HTMX)**
            When an HTMX action fires, the framework calls
            ``page.initialize(copy=True, body_params=...)`` to rebuild the full widget
            tree with form-body data. Fields annotated with ``BodyParam`` are populated
            (keyed by ``<instance_id>-<param_name>``). The framework then locates the
            target widget in the tree, calls its ``_call_callback()`` method, and renders
            only the widgets returned by the framework user's callback with
            ``hx_swap_oob=True`` for partial-page updates.

        Parameters
        ----------
        copy
            When ``True``, produce a deep copy of this widget via Pydantic's
            ``model_copy`` before applying any mutations. Should be ``True`` for the
            root page widget so the registered prototype is never mutated between
            requests.
        update
            Explicit field overrides applied before request-parameter extraction.
        query_params
            Raw query parameters from the incoming HTTP request, as returned by
            Starlette's ``request.query_params``.
        body_params
            Parsed form-body values from the incoming HTTP request.
        parent
            The parent widget in the tree. Set automatically during recursive
            initialisation; callers should not normally need to pass this.

        Returns
        -------
        The initialised widget (either a deep copy or ``self``, depending on
        ``copy``).

        TODO
        ----
        - Consider always copying and removing it from the public signature. However
          this did lead to issues with the List widgets in the past.
        - ``_build_hx_include`` inspects the callback signature to derive CSS
          selectors — this could be computed once at registration time instead of
          on every request.
        - ``BodyParam`` lookup relies on ``<instance_id>-<param_name>`` naming
          convention shared with the HTML templates; formalise this contract.
        """
        # Set the parent reference before any copying so it is available downstream.
        if parent is not None:
            self.parent = parent

        # Either produce a deep copy with Pydantic's model_copy, or mutate in place.
        if copy:
            new_instance = super().model_copy(deep=True, update=update)
        else:
            new_instance = self
            if update is not None:
                for k, v in update.items():
                    setattr(new_instance, k, v)

        # Apply any field values sourced from URL query parameters.
        if query_params is not None:
            query_parameters = self._extract_query_parameters(query_params=query_params)
            for k, v in query_parameters.items():
                setattr(new_instance, k, v)

        # Apply any field values sourced from the request body.
        if body_params is not None:
            body_parameters = self._extract_body_parameters(
                body_params=body_params,
                instance_id=new_instance.id,
            )
            for k, v in body_parameters.items():
                setattr(new_instance, k, v)

        # Build the child widget tree, propagating request params and parent reference
        # recursively so every descendant is initialised with the same context.
        children = new_instance.compose()
        for child in children:
            child.initialize(
                copy=False,
                query_params=query_params,
                body_params=body_params,
                parent=new_instance,
            )

        new_instance.children = children

        # Resolve the hx-include list now that the full child tree is available.
        new_instance._build_hx_include()

        return new_instance

    @classmethod
    def _extract_query_parameters(
        cls, query_params: Mapping[str, list[str]]
    ) -> dict[str, Any]:
        """
        Extract field values from query parameters for fields annotated with `QueryParam`.

        Parameters
        ----------
        query_params
            Mapping of query parameter names to lists of string values from the request.

        Returns
        -------
        Mapping of model field names to their extracted values. List-typed fields
        receive the full list of query parameters; all other fields receive the first
        value.
        """
        query_parameters: dict[str, Any] = {}

        for k, v in cls.model_fields.items():
            if len(v.metadata) == 0:
                continue

            query_param = next(
                (m for m in v.metadata if isinstance(m, QueryParam)), None
            )

            if query_param is not None:
                query_param_name = query_param.get_query_param_name() or k
                value_from_request = query_params.get(query_param_name, [])

                if len(value_from_request) == 0:
                    continue

                # Ignoring the ruff error about type comparisons here since it seems
                # to be not fitting to our use case. TODO: double check.
                if get_origin(v.annotation) == list:  # noqa: E721
                    query_parameters[k] = value_from_request
                else:
                    query_parameters[k] = value_from_request[0]

        return query_parameters

    @classmethod
    def _extract_body_parameters(
        cls, body_params: Mapping[str, Any], instance_id: str
    ) -> dict[str, Any]:
        """
        Extract field values from body parameters for fields annotated with `BodyParam`.

        Parameters
        ----------
        body_params
            Mapping of body parameter names to their values from the request.
        instance_id
            The widget instance ID, prepended to each parameter name when looking up
            values in ``body_params``.

        Returns
        -------
        Mapping of model field names to their extracted values.
        """
        body_parameters: dict[str, Any] = {}

        for k, v in cls.model_fields.items():
            if len(v.metadata) == 0:
                continue

            body_param = next((m for m in v.metadata if isinstance(m, BodyParam)), None)

            if body_param is not None and body_params is not None:
                body_param_name = body_param.get_body_param_name() or k
                body_param_name = instance_id + "-" + body_param_name

                body_value = body_params.get(body_param_name, None)
                if body_value is None:
                    continue

                body_parameters[k] = body_value

        return body_parameters

    def get_all_children(
        self,
        type: Type[W],
    ) -> list[W]:
        children_of_type = [
            widget.initialize() for widget in self.children if isinstance(widget, type)
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
                    widget_copy = widget.initialize()
                    return widget_copy

        remaining_id = "/".join(id_split[1:])

        for widget in children_of_type:
            if widget.id == id_split[0]:
                widget_copy = widget.initialize()

                return widget_copy.get_child_widget(
                    type=type,
                    id=remaining_id,
                )

        raise ValueError(f"Widget not found: {type} with id {id}")

    def get_additional_context(self) -> dict[str, Any]:
        additional_context = super().get_additional_context()

        children_instances = [
            child.initialize(update={"parent": self}) for child in self.children
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
