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
