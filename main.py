from typing import Annotated, Iterable
from math import sin, cos

from newsflash.elements import (
    FunctionRegistry,
    Button,
    InputInteger,
    Element,
    Paragraph,
    Header,
    Plot,
    Horizontal,
)
from newsflash.app import NewsflashApp


functions = FunctionRegistry()


@functions.add(on=Button(id="submit-btn").click())
def recreate_sine_plot(
    input_a: Annotated[InputInteger, "input-a"],
    line_plot: Annotated[Plot, "line-plot"],
) -> Iterable[Element]:
    fig, ax = line_plot.create_figure()

    ax.plot(
        [x / 10 for x in range(300)],
        [sin(x / 10) * input_a.value for x in range(300)],
        linewidth=3,
        color="#931f1f",
        label="sine",
    )
    ax.plot(
        [x / 10 for x in range(300)],
        [cos(x / 10) * input_a.value for x in range(300)],
        linewidth=3,
        color="green",
        label="cosine",
    )
    ax.set_title("Sine Wave Plot")
    ax.legend()

    line_plot.set_figure(figure=fig)

    yield line_plot


class NumbersApp(NewsflashApp):
    def compose(self) -> Iterable[Element]:
        yield Header(id="page-header", text="Sine Plot")
        yield Paragraph(id="input-label", text="Enter the amplitude of the sine wave:")

        yield Horizontal(
            id="horizontal-inputs",
            children=[
                InputInteger(id="input-a"),
                Button(id="submit-btn", label="Regenerate Plot"),
            ],
        )

        yield Horizontal(
            id="horizontal-plot",
            children=[
                Plot(id="line-plot"),
            ],
        )


app = NumbersApp(functions=functions)
