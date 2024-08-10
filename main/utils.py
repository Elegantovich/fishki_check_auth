import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

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
