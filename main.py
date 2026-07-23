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


def build_line_plot(
    line_plot: Plot,
    sine_wave_amplitude: int,
    cosine_wave_amplitude: int,
) -> Plot:
    fig, ax = line_plot.create_figure()

    ax.plot(
        [x / 10 for x in range(300)],
        [sin(x / 10) * sine_wave_amplitude for x in range(300)],
        linewidth=3,
        color="#931f1f",
        label="sine",
    )
    ax.plot(
        [x / 10 for x in range(300)],
        [cos(x / 10) * cosine_wave_amplitude for x in range(300)],
        linewidth=3,
        color="green",
        label="cosine",
    )
    ax.set_title("A sine and a cosine")
    ax.legend()

    line_plot.set_figure(figure=fig)
    return line_plot


@functions.add(
    on=[
        Plot(id="line-plot").revealed(),
        Button(id="submit-btn").click(),
        InputInteger(id="sine-wave-amplitude").input(),
        InputInteger(id="cosine-wave-amplitude").input(),
    ]
)
def recreate_sine_plot(
    sine_wave_amplitude: Annotated[InputInteger, "sine-wave-amplitude"],
    cosine_wave_amplitude: Annotated[InputInteger, "cosine-wave-amplitude"],
    line_plot: Annotated[Plot, "line-plot"],
) -> Iterable[Element]:
    yield build_line_plot(
        line_plot=line_plot,
        sine_wave_amplitude=sine_wave_amplitude.value,
        cosine_wave_amplitude=cosine_wave_amplitude.value,
    )


@functions.add(on=Button(id="submit-btn").click())
def reset_inputs(
    line_plot: Annotated[Plot, "line-plot"],
) -> Iterable[Element]:
    yield InputInteger(id="sine-wave-amplitude", value=5)
    yield InputInteger(id="cosine-wave-amplitude", value=7)
    yield build_line_plot(
        line_plot=line_plot,
        sine_wave_amplitude=5,
        cosine_wave_amplitude=7,
    )


class InputsRow(Horizontal):
    id: str = "horizontal-inputs"

    def compose(self) -> Iterable[Element]:
        yield InputInteger(id="sine-wave-amplitude", value=5)
        yield InputInteger(id="cosine-wave-amplitude", value=7)
        yield Button(id="submit-btn", label="Reset Inputs")


class NumbersApp(NewsflashApp):
    def compose(self) -> Iterable[Element]:
        yield Header(id="page-header", text="Sines and Cosines")
        yield Paragraph(id="inputs-label", text="Enter the amplitude for the waves:")
        yield InputsRow()
        yield Plot(id="line-plot")


app = NumbersApp(functions=functions)
