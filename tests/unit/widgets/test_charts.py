from unittest.mock import patch

from newsflash.widgets.widgets import Widget, WidgetContainer
from newsflash.widgets.charts import Chart


def test_default_on_load():
    chart = Chart()
    assert chart.on_load() == []


def test_render_content_calls_super():
    chart = Chart()
    with patch.object(Widget, "render") as mock_render:
        chart.render_content()
        mock_render.assert_called_once()


def test_render_container():
    class DummyChart(Chart):
        id: str = "dummy-chart"
    
    chart = DummyChart()

    def new_render(self) -> str:
        return f"<div id={self.widget_id}></div>"

    with patch.object(WidgetContainer, "render", new=new_render):
        rendered = chart.render_container()

    assert rendered == "<div id=dummy-chart></div>"
