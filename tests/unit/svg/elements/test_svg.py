from newsflash.svg.element import Element
from newsflash.svg.elements import SVG


class DummyElement(Element):
    def render(self) -> str:
        return "<dummy></dummy>"


def test_svg_initialization():
    svg = SVG(width=200, height=100)
    assert svg.width == 200
    assert svg.height == 100
    assert svg.elements == []


def test_svg_append():
    svg = SVG(width=200, height=100)
    element = DummyElement()
    svg.append(element)
    assert len(svg.elements) == 1
    assert element in svg.elements


def test_svg_render():
    svg = SVG(id="test-svg", width=200, height=100)
    element = DummyElement()
    svg.append(element)

    result = svg.render()
    expected = """<svg
    xmlns="http://www.w3.org/2000/svg" 
    id="test-svg"
    class="" 
    width="200.0"
    height="100.0"
    viewBox="0 0 200.0 100.0"
    style=""
>
    <dummy></dummy>
</svg>"""
    assert result == expected


def test_svg_render_swap_oob():
    svg = SVG(id="test-svg", width=200, height=100)
    svg.hx_swap_oob = True
    element = DummyElement()
    svg.append(element)

    result = svg.render()
    expected = """<svg
    xmlns="http://www.w3.org/2000/svg" 
    id="test-svg"
    class="" 
    width="200.0"
    height="100.0"
    viewBox="0 0 200.0 100.0"
    style=""
    hx-swap-oob="true"
>
    <dummy></dummy>
</svg>"""
    assert result == expected
