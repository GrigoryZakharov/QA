import pytest
import allure
import logging

logger = logging.getLogger(__name__)

@allure.feature("Drag and Drop Elements")
@allure.story("Проверка перетаскивания элементов")
@allure.severity(allure.severity_level.NORMAL)
class TestDragAndDropElements:

    @pytest.fixture(autouse=True)
    def setup(self, drag_and_drop_page):
        """Фикстура для подготовки теста"""
        self.page = drag_and_drop_page
        yield

    @allure.title("Перетаскивание элемента A в B")
    def test_drag_and_drop_A_to_B(self):
        """Тест контекстного меню по правому клику"""
        with allure.step("Открыть страницу Drag and Drop Elements"):
            self.page.open()
        with allure.step("Перетащить элемент A в B"):
            self.page.drag_and_drop("A", "B")

    logger.info(" Test passed: Element A dragged to B successfully")

    @allure.title("Перетаскивание элемента B в A")
    def test_drag_and_drop_B_to_A(self):
        """Тест контекстного меню по правому клику"""
        with allure.step("Открыть страницу Drag and Drop Elements"):
            self.page.open()
        with allure.step("Перетащить элемент B в A"):
            self.page.drag_and_drop("B", "A")
    logger.info(" test passed: Element B dragged to A successfully")