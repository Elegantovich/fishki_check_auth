import logging
import logging.config
from app.base_app import BaseApplication


import pytest

log = logging.getLogger(__name__)


@pytest.fixture()
def app():
    app = BaseApplication()
    yield app
    app.destroy()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call':
        if report.failed:
            log.error(report.longreprtext)
            log.critical(f'<<< FAILED: {report.duration:.4f} <<<')
            item.funcargs["app"].robot.make_screenshot(f"_{item.originalname}")
