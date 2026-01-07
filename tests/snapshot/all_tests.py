from typing import Type

from .snapshot_test import SnapshotTest, AllSnapshotsPass
from .bar_chart import ascending


def get_all_tests() -> dict[str, Type[SnapshotTest]]:
    all_tests = [
        ascending.AscendingBarChart5,
        ascending.AscendingBarChart20,
    ]

    return {test.name: test for test in all_tests}


def get_test_by_name(name: str) -> Type[SnapshotTest]:
    if name == "":
        return AllSnapshotsPass

    all_tests = get_all_tests()
    return all_tests[name]


def get_next_failing_test() -> Type[SnapshotTest]:
    for test in get_all_tests().values():
        if not test.passes_test():
            return test

    return AllSnapshotsPass
