from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions


def get_web_driver():
    """Get driver"""
    driver = None
    options = ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver
