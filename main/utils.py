import logging
import os
from configs.config import Config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import coloredlogs

_log = logging.getLogger(__name__)

FORMAT = '[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s'
DATE_FORMAT = '%H:%M:%S'


def get_web_driver():
    """Get driver"""
    driver = None
    options = ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver


def colored_message(logger, level, msg, settings: dict = None):
    base_level = logging.getLogger().level
    if os.getenv('CUSTOM_TERMINAL') == '1':
        prev_settings = coloredlogs.DEFAULT_LEVEL_STYLES.copy()
        for lvl in coloredlogs.DEFAULT_LEVEL_STYLES:
            coloredlogs.DEFAULT_LEVEL_STYLES[lvl] = settings
        coloredlogs.install(logger=logger, level=base_level, fmt=FORMAT, datefmt=DATE_FORMAT)

        logger.log(level=level, msg=msg)

        coloredlogs.DEFAULT_LEVEL_STYLES = prev_settings
        coloredlogs.install(logger=logger, level=base_level, fmt=FORMAT, datefmt=DATE_FORMAT)
    else:
        logger.log(level=level, msg=msg)
