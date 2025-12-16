import pytest
import allure
import logging

logger = logging.getLogger(__name__)

@allure.feature("Broken Images")
@allure.story("Проверка сломанных изображений на странице")
@allure.severity(allure.severity_level.NORMAL)
class TestBrokenImg:

    @pytest.fixture(autouse=True)
    def setup(self, broken_img_page):
        """Фикстура для подготовки теста"""
        self.page = broken_img_page
        yield

    @allure.title("Проверка сломанных изображений на странице")
    def test_broken_img(self):
        """Тест проверки сломанных изображений на странице"""
        with allure.step("Открыть страницу Broken Images"):
            self.page.open()

        with allure.step("Проверить наличие сломанных изображений"):
            assert self.page.check_images() is not None, "Сломанные изображения не найдены"
        
        logger.info("Test passed: Broken images detected successfully")

    @allure.title("Проверка общего количества изображений на странице")
    def test_total_images_count(self):
        """Тест получения общего количества изображений на странице"""
        with allure.step("Открыть страницу Broken Images"):
            self.page.open()

        with allure.step("Получить общее количество изображений"):
            total_images = self.page.get_total_images_count()
            assert total_images > 0, "Изображения на странице не найдены"

        logger.info("Test passed: Total images count retrieved successfully")