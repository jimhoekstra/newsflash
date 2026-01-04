from typing import Type
from pathlib import Path

from newsflash.app import App, Page
from newsflash.widgets import HTML, Button, Select, ValueDisplay
from newsflash.widgets.widgets import Widget

from .bar_chart import ascending
from .snapshot_test import SnapshotTest


def get_all_tests() -> dict[str, Type[SnapshotTest]]:
    all_tests = [
        ascending.TestAscendingBarChart5,
        ascending.TestAscendingBarChart20,
    ]

    return {test.name: test for test in all_tests}


class TestSelect(Select):
    id: str = "test-select"
    options: list[str] = list(get_all_tests().keys())

    def on_select(
        self,
        snapshot: "SnapshotHTML",
        test_description: "TestDescription",
    ) -> list[Widget]:
        assert self.selected is not None
        test_class = get_all_tests()[self.selected]

        snapshot.html_content = test_class.render()
        test_description.value = test_class.description
        return [snapshot, test_description]


class SnapshotHTML(HTML):
    id: str = "snapshot-html"
    html_content: str = "<p>The snapshot will be displayed here.</p>"


class TestDescription(ValueDisplay):
    id: str = "test-description"
    label: str = "Test Description"
    value: str = "The test description will be displayed here."


class ApproveButton(Button):
    id: str = "approve-button"
    label: str = "Approve Snapshot"

    def on_click(
        self, 
        test_select: TestSelect,
        snapshot: SnapshotHTML,
    ) -> list[Widget]:
        assert test_select.selected is not None
        test_class = get_all_tests()[test_select.selected]

        if test_class.passes_test(snapshot.html_content):
            print(f"Snapshot for test '{test_select.selected}' already approved.")
        else:
            test_class.save_rendered(snapshot.html_content)
            print(f"Snapshot for test '{test_select.selected}' approved and saved.")

        return []


page = Page(
    id="",
    path="/",
    title="Snapshot Test",
    template=("snapshot", "page.html"),
    children=[
        TestSelect(),
        SnapshotHTML(),
        TestDescription(),
        ApproveButton(),
    ],
)

app = App(
    pages=[page],
    template_folders=[
        ("snapshot", Path(__file__).parent / "templates" / "snapshot"),
    ]
)
