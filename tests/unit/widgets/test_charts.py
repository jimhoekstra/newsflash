from unittest.mock import patch

from newsflash.widgets.widgets import WidgetContainer
from newsflash.widgets.charts import Chart


def test_default_on_load():
    chart = Chart()
    assert chart.on_load() == []


def test_render_container():
    class DummyChart(Chart):
        id: str = "dummy-chart"

    chart = DummyChart()

    def new_render(self, *args, **kwargs) -> str:
        return f"<div id={self.widget_id}></div>"

    with patch.object(WidgetContainer, "render", new=new_render):
        rendered = chart.render()

    assert rendered == "<div id=dummy-chart></div>"
