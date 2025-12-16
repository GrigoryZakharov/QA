from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from retrying import retry
import logging

logger = logging.getLogger(__name__)

class DynamicContentPage:
    """Page Object для страницы dynamic content Elements"""
    
    """Локаторы"""
    CONTENT_ELEMENTS = (By.CLASS_NAME, "large-10")
    PAGE_LOADED_INDICATOR = (By.ID, "content")


    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "https://the-internet.herokuapp.com/dynamic_content?with_content=static"    
    
    def open(self, static = False):
        """Открыть страницу с опциональным статическим контентом"""
        url = self.url
        if static:
            url += "&with_content=static"
        self.driver.get(url)
        self._wait_for_page_load()
        logger.info(f"page opened: {url}")
        return self

    def _wait_for_page_load(self):
        """Дождаться загрузки страницы"""
        try:
            self.wait.until(EC.presence_of_element_located(self.PAGE_LOADED_INDICATOR))
            self.wait.until(EC.presence_of_all_elements_located(self.CONTENT_ELEMENTS))
        except TimeoutException:
            logger.error(" page did not load within the expected time")
            raise

    def get_content_texts(self):
            """Получить тексты всех динамических элементов"""
            elements = self.driver.find_elements(*self.CONTENT_ELEMENTS)
            texts = [element.text.strip() for element in elements if element.text.strip()]
            logger.debug(f"Got {len(texts)} content texts")
            return texts

    @retry(stop_max_attempt_number=3, 
       wait_fixed=1000,
       retry_on_exception=lambda x: isinstance(x, StaleElementReferenceException))
    def refresh_and_get_content(self):
        """Обновить страницу и получить новый контент"""
        initial_texts = self.get_content_texts()
        logger.info(f"content after update: {len(initial_texts)} elements")

        self.driver.refresh()
        self._wait_for_page_load()

        new_texts = self.get_content_texts()
        logger.info(f"content before update: {len(new_texts)} elements")
        return initial_texts, new_texts
    
    def is_content_dynamic(self, max_attempts=3):

        for attempt in range(1, max_attempts + 1):
            initial_texts, new_texts = self.refresh_and_get_content()

            if initial_texts != new_texts:
                logger.info(" Dynamic content has changed successfully.")
                return True
            
            logger.warning(f"Attempt {attempt} did not show content change. Retrying...")

        logger.error(f" Dynamic content didn't change after {max_attempts} page updates.")
        return False



    def check_for_dynamic_content_change(self):
        """Проверить изменение динамического контента"""
        initial_contents = [
            element.text for element in self.driver.find_elements(By.CLASS_NAME, "large-10")
        ]
        
        self.driver.refresh()
        
        refreshed_contents = [
            element.text for element in self.driver.find_elements(By.CLASS_NAME, "large-10")
        ]
        
        assert initial_contents != refreshed_contents, " Динамический контент не изменился после обновления страницы"
        return self