from .all_tests import get_all_tests


def test_snapshots():
    for snapshot_test in get_all_tests().values():
        assert snapshot_test.passes_test(), (
            "Snapshot test failed. Please run the snapshot test approval app and review the changes."
        )
