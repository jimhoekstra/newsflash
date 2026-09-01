from typing import Iterable
from math import sin, cos

from newsflash.elements import (
    Button,
    InputInteger,
    Select,
    Element,
    Paragraph,
    Header,
    Plot,
    Horizontal,
)
from newsflash.functions import FunctionRegistry
from newsflash.app import NewsflashApp


functions = FunctionRegistry()


class LinePlot(Plot):
    id: str = "line-plot"


class SineWaveAplitudeInput(InputInteger):
    id: str = "sine-wave-amplitude"
    value: int = 5


class CosineWaveAplitudeSelect(Select):
    id: str = "cosine-wave-amplitude"
    options: list[int] = [2, 7, 27, 49]
    selected: int = 7


class ResetInputsButton(Button):
    id: str = "reset-inputs-btn"
    label: str = "Reset Inputs"


def _build_line_plot(
    line_plot: LinePlot,
    sine_wave_amplitude: int,
    cosine_wave_amplitude: int,
) -> LinePlot:
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
    # A single function can have multiple triggers.
    on=[
        LinePlot().revealed(),
        SineWaveAplitudeInput().input(),
        CosineWaveAplitudeSelect().select(),
    ]
)
def recreate_sine_plot(
    sine_wave_amplitude: SineWaveAplitudeInput,
    cosine_wave_amplitude: CosineWaveAplitudeSelect,
    line_plot: LinePlot,
) -> Iterable[Element]:
    # Rebuild the line plot given the updated input values.
    yield _build_line_plot(
        line_plot=line_plot,
        sine_wave_amplitude=sine_wave_amplitude.value,
        cosine_wave_amplitude=cosine_wave_amplitude.selected,
    )


# Example that shows the same trigger, in this case an input trigger on the
# SineWaveAmplitudeInput element, can trigger multiple functions (this one,
# in addition to recreate_sine_plot above).
@functions.add(on=SineWaveAplitudeInput().input())
def log_sine_wave_amplitude_input_event(
    sine_wave_amplitude: SineWaveAplitudeInput,
) -> Iterable[Element]:
    # Log a message
    print(f"User submitted new sine wave amplitude input: {sine_wave_amplitude.value}")

    # Return nothing, since this function does not change anything in the UI.
    return []


@functions.add(on=ResetInputsButton().click())
def reset_inputs(
    line_plot: LinePlot,
) -> Iterable[Element]:
    sine_wave_amplitude_input = SineWaveAplitudeInput()
    cosine_wave_amplitude_select = CosineWaveAplitudeSelect()

    yield sine_wave_amplitude_input
    yield cosine_wave_amplitude_select
    yield _build_line_plot(
        line_plot=line_plot,
        sine_wave_amplitude=sine_wave_amplitude_input.value,
        cosine_wave_amplitude=cosine_wave_amplitude_select.selected,
    )


class InputsRow(Horizontal):
    id: str = "horizontal-inputs"

    def compose(self) -> Iterable[Element]:
        yield SineWaveAplitudeInput()
        yield CosineWaveAplitudeSelect()
        yield ResetInputsButton()


class NumbersApp(NewsflashApp):
    def compose(self) -> Iterable[Element]:
        # You can use generic Element types like Header and Paragraph, as long
        # as you pass all the required inputs (like `id`) to the constructor.
        yield Header(id="page-header", text="Sines and Cosines")
        yield Paragraph(id="inputs-label", text="Enter the amplitude for the waves:")

        # You can also nest elements, like in this example using InputsRow
        yield InputsRow()
        yield Paragraph(id="selected-log")

        # Lastly, you can yield your custom Element types, like LinePlot. The
        # advantage of this is that the LinePlot type can be reused across other
        # elements and function so that you don't depend on reconstructing generic
        # plots with the same ID every time.
        yield LinePlot()


app = NumbersApp(functions=functions)
