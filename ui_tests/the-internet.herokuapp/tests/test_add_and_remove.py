import pytest
import allure
import logging

logger = logging.getLogger(__name__)

@allure.feature("Add/Remove Elements")
@allure.story("Проверка добавления и удаления элементов")
@allure.severity(allure.severity_level.NORMAL)
class TestAddAndRemoveElements:

    @pytest.fixture(autouse=True)
    def setup(self, add_and_remove_page):
        """Фикстура для подготовки теста"""
        self.page = add_and_remove_page
        yield

    @allure.title("Добавление элемента на странице")
    def test_add_element(self):
        with allure.step("Открыть страницу Add/Remove Elements"):
            self.page.open()
    
        with allure.step("Добавить один элемент"):
            self.page.add_element()

        with allure.step("Проверить что элемент добавлен"):
            assert self.page.get_elements_count() == 1, "Элемент не был добавлен"
        
        logger.info("Test passed: Element added successfully")


    @allure.title("Добавление нескольких элементов на странице")
    def test_add_multiple_elements(self):
        with allure.step("Открыть страницу Add/Remove Elements"):
            self.page.open()

        with allure.step("Добавить три элемента"):
            self.page.add_element(3)

        with allure.step("Проверить что три элемента добавлены"):
            assert self.page.get_elements_count() == 3, "Элементы не были добавлены"

        logger.info("Test passed: Multiple elements added successfully")

    @allure.title("Удаление элемента со страницы")
    def test_add_and_remove_element(self):
        with allure.step("Открыть страницу Add/Remove Elements"):
            self.page.open()

        with allure.step("Добавить два элемента"):
            self.page.add_element(2)

        with allure.step("Удалить один элемент"):
            self.page.delete_element(0)

        with allure.step("Проверить что остался один элемент"):
            assert self.page.get_elements_count() == 1, "Элемент не был удален"

        logger.info("Test passed: Element removed successfully")

    @allure.title("Добавление и удаление всех элементов на странице")
    def test_add_and_remove_all_elements(self):
        with allure.step("Открыть страницу Add/Remove Elements"):
            self.page.open()

        with allure.step("Добавить три элемента и удалить все"):
            self.page.add_element(3).delete_all_elements()

        with allure.step("Проверить что все элементы удалены"):
            assert self.page.get_elements_count() == 0, "Не все элементы были удалены"

        logger.info("Test passed: All elements added and removed successfully")

    @allure.title("Попытка удаления несуществующего элемента")
    def test_delete_nonexistent_element(self):
        with allure.step("Открыть страницу Add/Remove Elements"):
            self.page.open()

        with allure.step("Попытаться удалить элемент когда их нет"):
            self.page.delete_element(0)  # Не должно быть ошибки

        with allure.step("Проверить что количество элементов осталось нулевым"):
            assert self.page.get_elements_count() == 0, "Количество элементов изменилось после попытки удаления несуществующего элемента"

        logger.info("Test passed: Handled deletion of nonexistent element gracefully")