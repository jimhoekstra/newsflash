from pytest import fixture

from newsflash.svg.element import Element, ElementGroup


class DummyElement(Element):
    element_number: int


@fixture
def element1() -> Element:
    return DummyElement(element_number=1)


@fixture
def element2() -> Element:
    return DummyElement(element_number=2)


@fixture
def element3() -> Element:
    return DummyElement(element_number=3)


def test_append(element1, element2):
    group = ElementGroup()

    group.append(element1)
    assert group.elements == [element1]

    group.append(element2)
    assert group.elements == [element1, element2]


def test_extend(element1, element2, element3):
    group1 = ElementGroup()
    group1.append(element1)

    group2 = ElementGroup()
    group2.append(element2)
    group2.append(element3)

    group1.extend(group2)

    assert group1.elements == [element1, element2, element3]
