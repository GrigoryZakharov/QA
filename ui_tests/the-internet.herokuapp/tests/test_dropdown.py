import pytest
import allure
import logging

logger = logging.getLogger(__name__)

@allure.feature("Dropdown Elements")
@allure.story("Проверка дропдауна")
@allure.severity(allure.severity_level.NORMAL)
class TestDropdown:

    @pytest.fixture(autouse=True)
    def setup(self, dropdown_page):
        """Фикстура для подготовки теста"""
        self.page = dropdown_page
        yield

    @allure.title("Проверка начального состояния дропдауна")
    def test_dropdown_initial_state(self):
        """Тест контекстного меню по правому клику"""
        with allure.step("Открыть страницу Dropdown"):
            self.page.open()
        with allure.step("Проверить начальное состояние дропдауна"):
            self.page.get_dropdown_state()
        logger.info("Test passed: Dropdown initial state verified successfully")

    @allure.title("Выбор опции 1 дропдауна")
    def test_dropdown_select_option_1(self):
        """"""
        with allure.step("Открыть страницу Dropdown"):
            self.page.open()
        with allure.step("Выбрать опцию 1 дропдауна"):
            self.page.select_option("1")
        logger.info("Test passed: Dropdown option 1 selected successfully")

    @allure.title("Выбор опции 2 дропдауна")
    def test_dropdown_select_option_2(self):
        """"""
        with allure.step("Открыть страницу Dropdown"):
            self.page.open()
        with allure.step("Выбрать опцию 2 дропдауна"):
            self.page.select_option("2")
        logger.info("Test passed: Dropdown option 2 selected successfully")