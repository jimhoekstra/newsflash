import typing
from inspect import Signature

from pydantic import ValidationError
from fastapi import Request, Response

from newsflash.models import Element, ID, FunctionInputDefinition, FunctionDefinition


def build_function_input_definition(
    arg_name: str, annotation: typing.Any
) -> FunctionInputDefinition | None:
    """Build a function input definition for a single function argument.

    Parameters
    ----------
    arg_name
        The name of the function argument
    annotation
        The type annotation of the function argument. This can be one of two types:
            - `typing.Annotated`, in which case the first argument is the
              actual element type. There should be one additional argument to
              the annotation that is of type ID and contains a reference to the
              ID of the element.
            - A fully specified `Element`, where fully specified means that it can
              be instantiated without requiring additional arguments to be passed
              to the constructor. This means that the `id` attribute should be
              defined on this subclass of `Element`.

    Returns
    -------
    The function input definition for this function argument.

    Raises
    ------
    pydantic.ValidationError
        When the type of `annotation` is `Element` but it can't be instantiated
        without additional arguments passed to the constructor.
    ValueError
        When either the element type or the element ID cannot be derived from
        the annotation.
    """
    origin = typing.get_origin(annotation)

    if origin == typing.Annotated:
        args = typing.get_args(annotation)
        element_type = args[0] if issubclass(args[0], Element) else None
        element_id: ID | None = next((arg for arg in args if isinstance(arg, ID)), None)

    elif issubclass(annotation, Element):
        element_type = annotation
        try:
            element_instance = element_type()  # type: ignore
            element_id = ID(id=element_instance.id)
        except ValidationError:
            element_id = None

    else:
        element_type = None
        element_id = None

    if element_type is None:
        return None

    if element_id is None:
        raise ValueError(f"element: {arg_name} is not sufficiently defined")

    return FunctionInputDefinition(
        arg_name=arg_name,
        element_type=element_type,
        element_id=element_id.id,
    )


def get_function_input_definitions(
    function_signature: Signature,
) -> list[FunctionInputDefinition]:
    """Get the function input definition for a function signature.

    Arguments
    ---------
    function_signature
        The function signature of the function for which to get the function
        input definitions

    Returns
    -------
    A list of function input definitions with one element for every parameter in
    the function signature.
    """
    function_inputs: list[FunctionInputDefinition] = []
    for arg_name, arg in function_signature.parameters.items():
        function_input_definition = build_function_input_definition(
            arg_name=arg_name, annotation=arg.annotation
        )
        if function_input_definition is not None:
            function_inputs.append(function_input_definition)

    return function_inputs


def get_function_request_object_param(function_signature: Signature) -> str | None:
    for arg_name, arg in function_signature.parameters.items():
        if arg.annotation == Request:
            return arg_name

    return None


def get_function_response_object_param(function_signature: Signature) -> str | None:
    for arg_name, arg in function_signature.parameters.items():
        if arg.annotation == Response:
            return arg_name

    return None


def build_function_inputs_from_data(
    function_definition: FunctionDefinition, 
    values: dict[str, str], 
    request: Request,
    response: Response,
) -> dict[str, Element | Request | Response | None]:
    """Collect all required inputs for a function given a dict of values.

    Parameters
    ----------
    function_definition
        The definition of the function for which to build the inputs.
    values
        The values to use when building the function inputs.

    Returns
    -------
    A dictionary mapping function argument names to that input
    argument's value.
    """
    function_inputs: dict[str, Element | Request | Response | None] = {}

    for function_input in function_definition.inputs:
        input_type = function_input.element_type

        input_values: dict[str, str] = {
            "id": function_input.element_id,
        }

        for input_key, input_value in values.items():
            input_id, input_parameter = input_key.split("--")
            if input_id == function_input.element_id:
                input_values[input_parameter] = input_value

        try:
            input_element = input_type.model_validate(input_values)
            input_element.set_fastapi_request_object(request=request)
            function_inputs[function_input.arg_name] = input_element
        except ValidationError:
            function_inputs[function_input.arg_name] = None
            # TODO: display validation error in the UI at the element's position
            print(f"Failed to parse input values for: {function_input.element_id}")

    if (request_object_param := function_definition.request_object_param) is not None:
        function_inputs[request_object_param] = request

    if (response_object_param := function_definition.response_object_param) is not None:
        function_inputs[response_object_param] = response

    return function_inputs
