from typing import Annotated, Iterable
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
from newsflash.models import ID
from newsflash.functions import FunctionRegistry
from newsflash.app import NewsflashApp


functions = FunctionRegistry()


class LinePlot(Plot):
    id: str = "line-plot"


class SineWaveAplitudeInput(InputInteger):
    id: str = "sine-wave-amplitude"
    value: int = 5


class CosineWaveAplitudeInput(InputInteger):
    id: str = "cosine-wave-amplitude"
    value: int = 7


class TestSelect(Select):
    id: str = "test-select"
    options: list[str ] =["Option A", "Option B", "Option C", "Option D"]
    selected: str = "Option A"


class ResetInputsButton(Button):
    id: str = "reset-inputs-btn"
    label: str = "Reset Inputs"


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
        LinePlot().revealed(),
        SineWaveAplitudeInput().input(),
        CosineWaveAplitudeInput().input(),
    ]
)
def recreate_sine_plot(
    sine_wave_amplitude: Annotated[InputInteger, ID("sine-wave-amplitude")],
    cosine_wave_amplitude: Annotated[InputInteger, ID("cosine-wave-amplitude")],
    line_plot: Annotated[Plot, ID("line-plot")],
) -> Iterable[Element]:
    yield build_line_plot(
        line_plot=line_plot,
        sine_wave_amplitude=sine_wave_amplitude.value,
        cosine_wave_amplitude=cosine_wave_amplitude.value,
    )


@functions.add(on=[
    TestSelect().select(),
    TestSelect().revealed(),
])
def log_select(
    select: TestSelect,
) -> Iterable[Element]:
    yield Paragraph(
        id="selected-log",
        text=f"You have selected: '{select.selected}'"
    )


@functions.add(on=TestSelect().input())
def log_select_input(
    select: TestSelect,
) -> Iterable[Element]:
    print(select.selected)
    return []


@functions.add(on=ResetInputsButton().click())
def reset_inputs(
    line_plot: Annotated[Plot, ID("line-plot")],
) -> Iterable[Element]:
    yield SineWaveAplitudeInput()
    yield CosineWaveAplitudeInput()
    yield build_line_plot(
        line_plot=line_plot,
        sine_wave_amplitude=5,
        cosine_wave_amplitude=7,
    )


class InputsRow(Horizontal):
    id: str = "horizontal-inputs"
    wide: bool = True

    def compose(self) -> Iterable[Element]:
        yield SineWaveAplitudeInput()
        yield CosineWaveAplitudeInput()
        yield TestSelect()
        yield ResetInputsButton()


class NumbersApp(NewsflashApp):
    def compose(self) -> Iterable[Element]:
        yield Header(id="page-header", text="Sines and Cosines")
        yield Paragraph(id="inputs-label", text="Enter the amplitude for the waves:")
        yield InputsRow()
        yield Paragraph(id="selected-log")
        yield LinePlot()


app = NumbersApp(functions=functions)
