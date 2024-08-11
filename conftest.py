import logging
import os
from app.base_app import BaseApplication
from configs.config import Config
import shutil
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


@pytest.fixture(scope="session", autouse=True)
def clear_artefats():
    """Очистка папки со скринщотами и рез-ми тестирования для allure отчёта"""
    path_to_allure_data = os.path.join(Config.root_path, "results")
    [os.remove(os.path.join(path_to_allure_data, file)) for file in os.listdir(path_to_allure_data)]
    log.info("Данные для allure отчёта очищены успешно")
    shutil.rmtree(os.path.join(Config.root_path, "screenshots"), ignore_errors=True)
    log.info("Папка со скришотами очищена успешно")
