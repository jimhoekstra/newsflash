from typing import Type
from pathlib import Path

from newsflash.app import App, Page
from newsflash.widgets import HTML, Button, Select, ValueDisplay, Notifications
from newsflash.widgets.widgets import Widget

from .bar_chart import ascending
from .snapshot_test import SnapshotTest


def get_all_tests() -> dict[str, Type[SnapshotTest]]:
    all_tests = [
        ascending.TestAscendingBarChart5,
        ascending.TestAscendingBarChart20,
    ]

    return {test.name: test for test in all_tests}


class OldSnapshotHTML(HTML):
    id: str = "old-snapshot-html"
    html_content: str = ascending.TestAscendingBarChart5.load_rendered() or "<p>No snapshot exists.</p>"


class NewSnapshotHTML(HTML):
    id: str = "new-snapshot-html"
    html_content: str = ascending.TestAscendingBarChart5.render()


class TestSelect(Select):
    id: str = "test-select"
    options: list[str] = list(get_all_tests().keys())

    def on_select(
        self,
        old_snapshot: OldSnapshotHTML,
        new_snapshot: NewSnapshotHTML,
        test_description: "TestDescription",
        approve_button: "ApproveButton",
        notifications: Notifications,
    ) -> list[Widget]:
        assert self.selected is not None
        notifications.push(f"Selected test: {self.selected}")
        test_class = get_all_tests()[self.selected]

        old_snapshot.html_content = test_class.load_rendered() or "<p>No snapshot exists.</p>"

        new_snapshot.html_content = test_class.render()
        test_description.value = test_class.description

        if test_class.passes_test():
            approve_button.label = "Snapshots Already Match"
            approve_button.disabled = True
        else:
            approve_button.label = "Approve Snapshot"
            approve_button.disabled = False
        
        return [old_snapshot, new_snapshot, test_description, approve_button, notifications]


class TestDescription(ValueDisplay):
    id: str = "test-description"
    label: str = "Test Description"
    value: str = ascending.TestAscendingBarChart5.description


class ApproveButton(Button):
    id: str = "approve-button"
    label: str = "Approve Snapshot" if not ascending.TestAscendingBarChart5.passes_test() else "Snapshots Already Match"
    disabled: bool = ascending.TestAscendingBarChart5.passes_test()

    def on_click(
        self, 
        test_select: TestSelect,
        snapshot: NewSnapshotHTML,
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
    title="Snapshot Test Viewer",
    template=("snapshot", "page.html"),
    children=[
        TestSelect(),
        OldSnapshotHTML(),
        NewSnapshotHTML(),
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
