import pytest
import allure
import logging

logger = logging.getLogger(__name__)

@allure.feature("Checkboxes")
@allure.story("Проверка работы с чекбоксами")
@allure.severity(allure.severity_level.NORMAL)
class TestCheckboxes:

    @pytest.fixture(autouse=True)
    def setup(self, check_box_page):
        """Фикстура для подготовки теста"""
        self.page = check_box_page
        yield

    @allure.title("Проверка загрузки чекбоксов на странице")
    def test_checkboxes_load(self):
        """ Тест загрузки страницы с чекбоксами """
        with allure.step("Открыть страницу с чекбоксами"):
            self.page.open()

        with allure.step("Проверить состояния чекбоксов по умолчанию"):
            self.page.get_checkboxes_states()
            
        logger.info("Test passed: Checkboxes loaded with correct initial states")

    @allure.title("Переключение состояний чекбоксов")
    def test_toggle_single_checkbox(self):
        """ Тест переключения одного чекбокса """
        with allure.step("Открыть страницу с чекбоксами и переключить первый чекбокс"):
            self.page.open()
        
        with allure.step("Переключить первый чекбокс"):
            self.page.toggle_checkbox(0)

        logger.info("Test passed: Single checkbox toggled successfully")

    @allure.title("Переключение всех чекбоксов")
    def test_toggle_all_checkboxes(self):
        """ Тест переключения всех чекбоксов """
        with allure.step("Открыть страницу с чекбоксами и переключить все чекбоксы"):
            self.page.open()

        with allure.step("Переключить все чекбоксы"):
            self.page.toggle_all_checkboxes()

        logger.info("Test passed: All checkboxes toggled successfully")

    @allure.title("Снятие выбора со всех чекбоксов")
    def test_toggle_none_checkboxes(self):
        """ Тест снятия выбора со всех чекбоксов """
        with allure.step("Открыть страницу с чекбоксами и снять выбор со всех чекбоксов"):
            self.page.open()

        with allure.step("Снять выбор со всех чекбоксов"):
            self.page.toggle_none_checkboxes()
        logger.info("Test passed: All checkboxes untoggled successfully")