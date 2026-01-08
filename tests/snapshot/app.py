from typing import Callable
from pathlib import Path

from newsflash.app import App, Page
from newsflash.widgets import HTML, Button, Select, ValueDisplay, Notifications
from newsflash.widgets.widgets import Widget

from .all_tests import get_all_tests, get_next_failing_test, get_test_by_name


class OldSnapshotHTML(HTML):
    id: str = "old-snapshot-html"
    html_content: str = get_next_failing_test().load_rendered()


class NewSnapshotHTML(HTML):
    id: str = "new-snapshot-html"
    html_content: str = get_next_failing_test().render()


class TestSelect(Select):
    id: str = "test-select"
    options: list[str] = list(get_all_tests().keys())
    default: Callable[[], str] = lambda: get_next_failing_test().name

    def on_select(
        self,
        old_snapshot: OldSnapshotHTML,
        new_snapshot: NewSnapshotHTML,
        test_description: "TestDescription",
        approve_button: "ApproveButton",
    ) -> list[Widget]:
        assert self.selected is not None
        test_class = get_test_by_name(self.selected)

        old_snapshot.html_content = test_class.load_rendered()
        new_snapshot.html_content = test_class.render()
        test_description.value = test_class.description

        if test_class.passes_test():
            approve_button.label = "Snapshots Already Match"
            approve_button.disabled = True
        else:
            approve_button.label = "Approve Snapshot"
            approve_button.disabled = False

        return [old_snapshot, new_snapshot, test_description, approve_button]


class NextChangedSnapshotButton(Button):
    id: str = "next-changed-snapshot-button"
    label: str = "Next Changed Snapshot"

    def on_click(
        self,
        test_select: TestSelect,
        test_description: "TestDescription",
        old_snapshot: OldSnapshotHTML,
        new_snapshot: NewSnapshotHTML,
        approve_button: "ApproveButton",
    ) -> list[Widget]:
        next_failing_test = get_next_failing_test()

        test_select.selected = next_failing_test.name
        return [
            test_select,
            *test_select.on_select(
                old_snapshot=old_snapshot,
                new_snapshot=new_snapshot,
                test_description=test_description,
                approve_button=approve_button,
            ),
        ]


class TestDescription(ValueDisplay):
    id: str = "test-description"
    label: str = "Test Description"
    value: str = get_next_failing_test().description


class ApproveButton(Button):
    id: str = "approve-button"
    label: str = (
        "Approve Snapshot"
        if not get_next_failing_test().passes_test()
        else "Snapshots Already Match"
    )
    disabled: bool = get_next_failing_test().passes_test()

    def on_click(
        self,
        test_select: TestSelect,
        old_snapshot: OldSnapshotHTML,
        new_snapshot: NewSnapshotHTML,
        notifications: Notifications,
    ) -> list[Widget]:
        assert test_select.selected is not None
        test_class = get_all_tests()[test_select.selected]

        if not test_class.passes_test(new_snapshot.html_content):
            test_class.save_rendered(new_snapshot.html_content)

            # Update the old snapshot content after approval
            old_snapshot.html_content = test_class.load_rendered()
            self.label = "Snapshots Already Match"
            self.disabled = True
            return [self, old_snapshot]

        else:
            notifications.push("Snapshots already match.")
            return [notifications]


page = Page(
    id="",
    path="/",
    title="Snapshot Test Viewer",
    template=("snapshot", "snapshot_test.html"),
    children=[
        TestSelect(),
        NextChangedSnapshotButton(),
        OldSnapshotHTML(),
        NewSnapshotHTML(),
        TestDescription(),
        ApproveButton(),
    ],
)

app = App(
    pages=[page],
    template_folders=[
        ("snapshot", Path(__file__).parent / "templates"),
    ],
)
