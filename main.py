from typing import Iterable
from math import sin, cos

from newsflash import NewsflashApp, FunctionRegistry
from newsflash.elements import (
    Button,
    InputInteger,
    Select,
    Element,
    Paragraph,
    Header,
    Plot,
    Horizontal,
    NotificationContainer,
    Notification,
)


class LinePlot(Plot):
    id: str = "line-plot"


class SineWaveAplitudeInput(InputInteger):
    id: str = "sine-wave-amplitude"
    value: int = 5


class CosineWaveAplitudeSelect(Select):
    id: str = "cosine-wave-amplitude"
    value: int = 7


class ResetInputsButton(Button):
    id: str = "reset-inputs-btn"
    label: str = "Reset Inputs"


functions = FunctionRegistry()


@functions.add(on=CosineWaveAplitudeSelect().search())
def get_cosine_amplitude_options(
    cosine_wave_amplitude: CosineWaveAplitudeSelect,
    sine_wave_amplitude: SineWaveAplitudeInput,
) -> Iterable[Element]:
    # This example shows that the options that are shown for a select
    # element can depend on the current status of other elements (i.e. the
    # value of sine_wave_amplitude in this case). Additionally, it can depend
    # on the current (typed) value of the select element itself to implement
    # custom search functionality.
    yield cosine_wave_amplitude.with_options(
        sorted([2, 7, 27, 49, sine_wave_amplitude.value])
    )


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
        cosine_wave_amplitude=cosine_wave_amplitude.value,
    )


# Ideally this update of resetting the select element (empty options, and updating
# to the selected value) would be handled by a function that is configured
# automatically.
@functions.add(on=CosineWaveAplitudeSelect().select())
def reset_cosine_select(
    cosine_wave_amplitude: CosineWaveAplitudeSelect,
) -> Iterable[Element]:
    yield cosine_wave_amplitude


@functions.add(on=ResetInputsButton().click())
def reset_inputs(
    line_plot: LinePlot,
    sine_wave_amplitude_input: SineWaveAplitudeInput,
    cosine_wave_amplitude_select: CosineWaveAplitudeSelect,
) -> Iterable[Element]:
    new_sine_wave_amplitude_input = SineWaveAplitudeInput()
    new_cosine_wave_amplitude_select = CosineWaveAplitudeSelect()

    sine_input_changed = (
        sine_wave_amplitude_input.value != new_sine_wave_amplitude_input.value
    )
    cosine_input_changed = (
        cosine_wave_amplitude_select.value != new_cosine_wave_amplitude_select.value
    )

    # Only rerender the inputs if the current values differ from the default values
    if sine_input_changed:
        yield new_sine_wave_amplitude_input

    if cosine_input_changed:
        yield new_cosine_wave_amplitude_select

    # Only rerender the plot if any of the inputs is different from the default values
    if sine_input_changed or cosine_input_changed:
        yield _build_line_plot(
            line_plot=line_plot,
            sine_wave_amplitude=new_sine_wave_amplitude_input.value,
            cosine_wave_amplitude=new_cosine_wave_amplitude_select.value,
        )
        yield Notification(message="Inputs have been reset")
    else:
        yield Notification(message="Inputs were already set to defaults")


class InputsLabels(Horizontal):
    id: str = "inputs-labels"

    def compose(self) -> Iterable[Element]:
        yield Paragraph(id="sine-input-label", text="Enter a sine wave amplitude:")
        yield Paragraph(id="cosine-input-label", text="And a cosine wave amplitude:")
        yield Paragraph(id="button-label", text="")


class InputsRow(Horizontal):
    id: str = "inputs-row"

    def compose(self) -> Iterable[Element]:
        yield SineWaveAplitudeInput()
        yield CosineWaveAplitudeSelect()
        yield ResetInputsButton()


class SineWavesApp(NewsflashApp):
    def compose(self) -> Iterable[Element]:
        # You can use generic Element types like Header, as long
        # as you pass all the required inputs (like `id`) to the constructor.
        yield Header(id="page-header", text="Sines and Cosines")

        # You can also nest elements, like in this example with InputsLabels
        # and InputsRow
        yield InputsLabels()
        yield InputsRow()

        # Lastly, you can yield your custom Element types, like LinePlot. The
        # advantage of this is that the LinePlot type can be reused across other
        # elements and function so that you don't depend on reconstructing generic
        # plots with the same ID every time.
        yield LinePlot()

        # Add the NotificationContainer element to the compose() of the app to enable
        # notifications for your app. It doesn't show anything by itself, but it does
        # allow you to return Notication() element from your functions and have those
        # show in the UI.
        yield NotificationContainer()


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
    ax.legend()

    line_plot.set_figure(figure=fig)
    return line_plot


app = SineWavesApp(functions=functions)
