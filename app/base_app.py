from configs.config import Config
from main.utils import get_web_driver
from robots.base_robot import BaseRobot
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait


class BaseApplication:
    def __init__(self):
        self.config = Config
        self.wd: WebDriver = get_web_driver()
        self.wd.implicitly_wait(self.config.timeout)
        self.robot = BaseRobot(self)

    def destroy(self):
        self.wd.quit()

    def get_webdriver_wait(self, timeout=Config.timeout, poll_frequency=0.5):
        return WebDriverWait(self.wd, timeout=timeout, poll_frequency=poll_frequency)
