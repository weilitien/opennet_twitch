import pytest

from utils.driver_factory import create_mobile_driver
from utils.screenshot import take_screenshot


# ── Driver fixture ────────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def driver():
    """
    Provide a fresh mobile-emulated Chrome driver for each test.
    Automatically quits after the test (pass or fail).
    """
    d = create_mobile_driver()
    yield d
    d.quit()


# ── Auto-screenshot on failure ─────────────────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a failure screenshot to the test report automatically."""
    outcome = yield
    report  = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            test_name = item.name.replace(" ", "_")
            path = take_screenshot(driver, f"FAILED_{test_name}")
            print(f"\n[conftest] failure screenshot → {path}")
