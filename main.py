from typing import Annotated, Iterable, Self

from newsflash.elements import (
    FunctionRegistry,
    Button,
    InputInteger,
    Element,
    Paragraph,
)
from newsflash.app import NewsflashApp


class AdditionResult(Paragraph):
    id: str = "addition-result"
    text: str = "The result is: unknown"

    def set_result(self, result: int) -> Self:
        self.text = f"The result is: {result}"
        return self


class SubmitButton(Button):
    label: str = "Submit"


functions = FunctionRegistry()


@functions.add(on=Button(id="submit-btn").click())
def add_numbers(
    input_a: Annotated[InputInteger, "input-a"],
    input_b: Annotated[InputInteger, "input-b"],
) -> Iterable[Element]:
    yield AdditionResult().set_result(input_a.value + input_b.value)


class NumbersApp(NewsflashApp):
    def compose(self) -> Iterable[Element]:
        yield InputInteger(id="input-a")
        yield InputInteger(id="input-b")
        yield SubmitButton(id="submit-btn")
        yield AdditionResult()


app = NumbersApp(functions=functions)
