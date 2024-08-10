import allure
from pages.base import BasePage
from selenium.webdriver.common.by import By


class MainPageLocators:
    button_form = (By.CSS_SELECTOR, "svg[baseProfile=tiny]")


class MainPage(BasePage):

    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.loc = MainPageLocators

    def open_page(self) -> None:
        self.open(self.url)

    @allure.step("Нажатие на кнопку 'Forms'")
    def button_form_click(self) -> None:
        self.get_obj(self.loc.button_form).click()

    @allure.step("Открыть форму регистрации")
    def open_register_form(self) -> None:
        self.button_form_click()
        self.show_zone_click()
