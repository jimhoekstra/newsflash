from typing import Any


from newsflash.svg.element import ElementGroup
from newsflash.svg.charts.barchart import build_barchart
from newsflash.svg.charts.linechart import build_linechart
from newsflash.svg.charts.histogram import build_histogram

from .widgets import Widget, WidgetContainer


class Chart(Widget):
    template: tuple[str, str] = ("svg", "svg.svg")
    width: float = 0.0
    height: float = 0.0
    title: str = ""
    title_font_size: int = 32
    label_font_size: int = 16

    elements: ElementGroup = ElementGroup()
    styles: dict[str, str] = {
        "position": "absolute",
    }

    _values_from_request: list[str] = ["width", "height"]
    _callback_fn_name: str = "on_load"

    def on_load(self, *args, **kwargs) -> list[Widget]:
        """Event handler for chart load events."""
        return []

    def render(self) -> str:
        container = WidgetContainer(
            widget_id=self.id,
        )
        container.hx_include.extend(self.hx_include)
        return container.render()

    def _render_update(self) -> str:
        return super().render()

    def get_additional_context(self) -> dict[str, Any]:
        additional_context = super().get_additional_context()
        additional_context.update(
            {
                "content": "\n    ".join(
                    element.render() for element in self.elements.elements
                ),
            }
        )
        return additional_context


class BarChart(Chart):
    def set_values(
        self,
        values: list[float] | list[int],
        labels: list[str],
    ) -> None:
        self.elements = build_barchart(
            values=values,
            labels=labels,
            width=self.width,
            height=self.height,
            title=self.title,
            title_font_size=self.title_font_size,
            label_font_size=self.label_font_size,
        )


class LineChart(Chart):
    classes: list[str] = ["line-chart"]

    def set_values(
        self,
        xs: list[float] | list[int],
        ys: list[float] | list[int],
    ) -> None:
        self.elements = build_linechart(
            xs=xs,
            ys=ys,
            width=self.width,
            height=self.height,
            title=self.title,
            title_font_size=self.title_font_size,
            label_font_size=self.label_font_size,
        )


class Histogram(Chart):
    def set_values(
        self,
        values: list[float] | list[int],
        num_bins: int,
    ) -> None:
        self.elements = build_histogram(
            values=values,
            num_bins=num_bins,
            width=self.width,
            height=self.height,
            title=self.title,
            title_font_size=self.title_font_size,
            label_font_size=self.label_font_size,
        )
