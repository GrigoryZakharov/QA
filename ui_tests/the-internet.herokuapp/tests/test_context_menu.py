import pytest
import allure
import logging

logger = logging.getLogger(__name__)

@allure.feature("Context Menu")
@allure.story("Проверка контекстного меню")
@allure.severity(allure.severity_level.NORMAL)
class TestAddAndRemoveElements:

    @pytest.fixture(autouse=True)
    def setup(self, context_menu_page):
        """Фикстура для подготовки теста"""
        self.page = context_menu_page
        yield

    @allure.title("Проверка контекстного меню по правому клику")
    def test_context_menu_right_click(self):
        """Тест контекстного меню по правому клику"""
        with allure.step("Открыть страницу Context Menu"):
            self.page.open()
        with allure.step("Кликнуть правой кнопкой мыши на квадрате и проверить алерт"):
            self.page.right_click_box()

        logger.info("Test passed: Context menu right click works successfully")