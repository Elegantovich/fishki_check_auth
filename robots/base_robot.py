import logging
import os
from datetime import datetime as dt
from pathlib import Path
from time import sleep

import allure
from configs.config import Config
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

log = logging.getLogger(__name__)


class BaseRobot:
    timeout = Config.timeout
    DTFORMAT = "%Y-%m-%d_%H:%M:%S"
    SCREEN_FOLDER_PATH = "./screenshots"

    def __init__(self, app):
        self.app = app
        self.attempts_count = 2500

    def open_url(self, url):
        """
        Загрузка веб-страницы.
        """
        log.info(f'Пытаюсь открыть страницу: {url}')
        self.app.wd.get(url)

    def fill(self, web_element, value=''):
        # перевод курсора в начало строки - иногда почему-то он оказывался не в начале
        sleep(0.5)
        web_element.send_keys(Keys.HOME)
        for _ in range(self.attempts_count):
            try:
                while value[-2:] not in web_element.get_attribute('value'):
                    web_element.send_keys(Keys.CONTROL + "a")
                    web_element.send_keys(Keys.DELETE)
                    return web_element.send_keys(value)
            except BaseException:
                pass

    def wait_for_element_clickable(self, locator, timeout=timeout,
                                   poll_frequency=0.5):
        """Динамическое ожидание кликабельного элемента"""
        return WebDriverWait(self.app.wd, timeout,
                             poll_frequency=poll_frequency).until(
                             ec.element_to_be_clickable(locator))

    def refresh_page(self):
        log.info('Обновляю страницу')
        self.app.wd.refresh()

    def make_screenshot(self, comment=""):
        """
        Создание папки screenshots если она не существует, формирование
        пути сохранения скриншота, сохранение скриншота, логирование,
        сохранение файла в allure
        """
        try:
            Path(self.SCREEN_FOLDER_PATH).mkdir(parents=True, exist_ok=True)
            path = (os.path.join(self.SCREEN_FOLDER_PATH,
                    f"{dt.now().strftime(self.DTFORMAT)}{comment}.gif"))
            if self.app.wd.save_screenshot(path):
                log.info(f"Скриншот успешно сохранен по пути: {path}")
                allure.attach.file(path, path, allure.attachment_type.GIF)
                sleep(1)
            else:
                log.info("Ошибка сохранения скриншота")
        except BaseException as error:
            log.info(f"Ошибка формирования скриншота: {error}")

    def move_to_element(self, element) -> None:
        self.app.wd.execute_script("arguments[0].scrollIntoView(true);", element)
