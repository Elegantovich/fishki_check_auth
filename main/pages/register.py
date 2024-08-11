import allure
from main.data.data import dict_gender
from main.pages.base import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class RegisterPageLocators:
    title_reg_form = (By.CSS_SELECTOR, "h1.text-center")
    first_name_field = (By.CSS_SELECTOR, "#firstName")
    last_name_field = (By.CSS_SELECTOR, "#lastName")
    email_field = (By.CSS_SELECTOR, "#userEmail")
    user_phone_number = (By.CSS_SELECTOR, "#userNumber")
    birth_date_field = (By.CSS_SELECTOR, "#dateOfBirthInput")
    bith_day = [By.CSS_SELECTOR, 'div.react-datepicker__day--0{0}']
    bith_month = (By.CLASS_NAME, 'react-datepicker__month-select')
    bith_year = (By.CLASS_NAME, 'react-datepicker__year-select')
    gender_male = (By.CSS_SELECTOR, "label[for=gender-radio-1]")
    gender_female = (By.CSS_SELECTOR, "label[for=gender-radio-2]")
    gender_other = (By.CSS_SELECTOR, "label[for=gender-radio-3]")
    submit_button = (By.CSS_SELECTOR, "div.text-right")
    success_title = (By.CSS_SELECTOR, "div.modal-title")
    personal_data_table = (By.XPATH, "//table[contains(@class, 'table')]/tbody/tr")


class RegisterPage(BasePage):
    def __init__(self, app):
        super().__init__(app)
        self.loc = RegisterPageLocators

    @allure.step("Заполнить форму регистрации")
    def fill_form(self, gender: int, **kwargs):
        assert self.check_item, "Заголовок формы рег-ии не найден"
        self.fill_name_field(kwargs["name"])
        self.fill_last_name_field(kwargs["last_name"])
        self.fill_email_field(kwargs["email"])
        self.select_gender(gender)
        self.fill_phone_number_field(kwargs["phone"])
        self.fill_birth_date(*kwargs["birth_data"])
        self.submit_button_click()

    @allure.step("Заполнить поле 'First Name'")
    def fill_name_field(self, name: str) -> None:
        self.app.robot.fill(self.get_obj(self.loc.first_name_field), name)

    @allure.step("Заполнить поле 'Last Name'")
    def fill_last_name_field(self, last_name: str) -> None:
        self.app.robot.fill(self.get_obj(self.loc.last_name_field), last_name)

    @allure.step("Заполнить поле 'email'")
    def fill_email_field(self, email: str) -> None:
        self.app.robot.fill(self.get_obj(self.loc.email_field), email)

    @allure.step("Заполнить поле 'Mobile Number'")
    def fill_phone_number_field(self, phone: str) -> None:
        self.app.robot.fill(self.get_obj(self.loc.user_phone_number), phone)

    @allure.step("Заполнить поле 'Date of Birth'")
    def fill_birth_date(self, day: str, month: str, year: str) -> None:
        self.get_obj(self.loc.birth_date_field).click()
        select_year = Select(self.get_obj(self.loc.bith_year))
        select_year.select_by_value(year)
        select_month = Select(self.get_obj(self.loc.bith_month))
        select_month.select_by_visible_text(month)
        self.loc.bith_day[1] = self.loc.bith_day[1].format(day)
        self.get_obj(self.loc.bith_day).click()

    @allure.step("Выбрать генерный признак: Male, Female: Other")
    def select_gender(self, gender: int):
        if gender == 0:
            self.get_obj(self.loc.gender_male).click()
        elif gender == 1:
            self.get_obj(self.loc.gender_female).click()
        else:
            self.get_obj(self.loc.gender_other).click()

    @allure.step("Нажатие на кнопку 'Submit'")
    def submit_button_click(self) -> None:
        self.app.robot.move_to_element(self.get_obj(self.loc.submit_button))
        self.get_obj(self.loc.submit_button).click()

    @allure.step("Проверить наличие фразы об успехе рег-ии")
    def check_success_registration(self) -> bool:
        return self.check_item(self.loc.success_title)

    @allure.step("Сверить УД с результатом")
    def check_personal_data(self, gender, **cred) -> bool:
        dict_data = {}
        for row in self.app.wd.find_elements(*self.loc.personal_data_table):
            items = row.find_elements(*(By.XPATH, ".//*"))
            if items[1].text not in (None, ""):
                dict_data[items[0].text] = items[1].text
        birth_data = cred["birth_data"]
        assert dict_data["Student Name"] == f"{cred['name']} {cred['last_name']}"
        assert dict_data["Student Email"] == cred['email']
        assert dict_data["Mobile"] == cred['phone']
        assert dict_data["Gender"] == dict_gender[gender]
        assert dict_data["Date of Birth"] == f"{birth_data[0]} {birth_data[1]},{birth_data[2]}"
