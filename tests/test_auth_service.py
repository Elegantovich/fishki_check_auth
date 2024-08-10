import allure
import pytest
from data.data import cred
from pages.main import MainPage
from pages.register import RegisterPage


class TestAuthService:

    @pytest.fixture(autouse=True)
    def main(self, app):
        self.main_page = MainPage(app)
        self.main_page.open_page()

    @pytest.fixture()
    def register(self, app):
        self.reg_page = RegisterPage(app)

    @pytest.mark.regress
    @pytest.mark.parametrize("gender", (0, 1, 2))
    @allure.description("Проверить цепочку регистрации")
    def test_registration(self, register, gender):
        self.main_page.open_register_form()
        self.reg_page.fill_form(gender, **cred)
        assert self.reg_page.check_success_registration(), "ошибка при регистрации"
        self.reg_page.check_personal_data(gender, **cred)
