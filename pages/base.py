import logging
import allure
from typing import Union
from app.base_app import BaseApplication
from configs.config import Config
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

log = logging.getLogger(__name__)


class BaseLocators:
    show_zone = (By.CSS_SELECTOR, "div.show")


class BasePage:
    url = Config.url
    timeout = Config.timeout
    base_loc = BaseLocators

    def __init__(self, app: BaseApplication):
        self.app = app

    def open(self, url: str) -> None:
        self.app.robot.open_url(url)

    def get_obj(self, locator: Union[tuple, list]):
        """Геттер для получения объекта по локатору"""
        return self.app.robot.wait_for_element_clickable(
            locator=locator,
            timeout=self.timeout)

    @allure.step("Нажатие на открывшуюся зону")
    def show_zone_click(self) -> None:
        self.get_obj(self.base_loc.show_zone).click()

    @allure.step("Проверить кликабельность веб-элемента")
    def check_item(self, loc: str) -> bool:
        try:
            self.get_obj(loc)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist
