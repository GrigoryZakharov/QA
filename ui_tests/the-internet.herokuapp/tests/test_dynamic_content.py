import pytest
import allure
import logging

logger = logging.getLogger(__name__)

@allure.feature("Dynamic Content")
@allure.story("Проверка динамического контента")
@allure.severity(allure.severity_level.NORMAL)
class TestDynamicContent:

    @pytest.fixture(autouse=True)
    def setup(self, dynamic_content_page):
        """Фикстура для подготовки теста"""
        self.page = dynamic_content_page
        yield

    @allure.title("Динамический контент должен меняться при обновлении страницы")
    def test_content_changes_on_refresh(self):
        """Тест проверяет что контент меняется при обновлении страницы"""
        with allure.step("Открыть страницу со статическим контентом"):
            self.page.open(static=True)

        with allure.step("Проверить что контент динамический"):
            is_dynamic = self.page.is_content_dynamic(max_attempts=5)

        with allure.step("Верифицировать результат"):
            assert is_dynamic, "Контент должен меняться при обновлении страницы"

        logger.info("Test passed: Dynamic content changes on refresh")


    @allure.title("Проверка количества элементов контента")
    def test_content_elements_count(self):
        """Тест проверяет что загружается ожидаемое количество элементов"""
        with allure.step("Открыть страницу"):
            self.page.open()

        with allure.step("Получить элементы контента"):
            texts = self.page.get_content_texts()
            
        with allure.step("Проверить количество элементов"):
            assert len(texts) >= 3, f"Ожидалось минимум 3 элемента, получено {len(texts)}"
            
        logger.info(f"Found {len(texts)} content elements on the page")
    
    @pytest.mark.parametrize("static_mode", [True, False])
    @allure.title("Проверка обоих режимов контента (статический/динамический)")
    def test_both_content_modes(self, static_mode):
        """Параметризованный тест для обоих режимов"""
        with allure.step(f"Открыть страницу в режиме static={static_mode}"):
            self.page.open(static=static_mode)
        
        with allure.step("Проверить загрузку контента"):
            texts = self.page.get_content_texts()
            assert len(texts) > 0, "Контент не загрузился"
            
        logger.info(f"Static mode={static_mode}: got {len(texts)} elements")