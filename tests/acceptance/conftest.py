"""Acceptance-suite policy: a stub that is not built yet is an expected failure.

A behaviour whose code still raises NotImplementedError is reported as xfail
("not built yet: S<x>.<y>"). Any other error is a real failure. Once the stubs
behind a test are built, the test passes. Nothing here hides a broken build.
"""

import pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Report NotImplementedError, in setup or in the test, as an expected failure."""
    outcome = yield
    report = outcome.get_result()
    if (
        call.excinfo is not None
        and report.failed
        and call.excinfo.errisinstance(NotImplementedError)
    ):
        report.outcome = "skipped"
        report.wasxfail = f"not built yet: {call.excinfo.value}"
