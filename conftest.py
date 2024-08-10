import logging
import logging.config
import os
from contextlib import contextmanager
from app.base_app import BaseApplication
from main.utils import colored_message as cl

import pytest

log = logging.getLogger(__name__)


@contextmanager
def _log_level_of_pytest_streamhandler(config, level: int = 60):
    """
    Если при запуске не была включена кастомная консоль(--cll) - сообщения conftest-логгера
    ниже чем <level> будут игнорироваться.
    Необходимо для отсечения кастомных сепарирущих лог-сообщений из conftest-логгера в лайв
    консоли pytest т.к. у нёё есть свои сепараторы:
    "------- live log setup ---------",
    "-------- live log call ---------"
    """
    logging_plugin = config.pluginmanager.get_plugin('logging-plugin')
    if os.getenv('CUSTOM_TERMINAL') != '1' and logging_plugin is not None:
        logging_plugin.log_cli_handler.setLevel(level)
        try:
            yield
        finally:
            logging_plugin.log_cli_handler.setLevel(log.level)
            return
    try:
        yield
    finally:
        pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    with _log_level_of_pytest_streamhandler(item.config):
        if report.when == 'call':
            if report.passed:
                passed_message = 'PASSED'
                if hasattr(report, 'wasxfail'):
                    passed_message = 'XPASS'
                cl(logger=log, level=logging.WARNING, msg=f'<<< {passed_message}: {report.duration:.4f} <<<',
                   settings=dict(color='green', bold=True))
            elif report.failed:
                log.error(report.longreprtext)
                log.critical(f'<<< FAILED: {report.duration:.4f} <<<')
                app = ([val for key, val in item.funcargs.items()
                        if '_app' in key.lower()][0])
                app.robot.make_screenshot(f"_{item.originalname}")
            elif report.skipped:
                log.error(report.longreprtext)
                log.critical(f'<<< XFAIL: {report.duration:.4f} <<<')


@pytest.fixture()
def app():
    app = BaseApplication()
    yield app
    app.destroy()
