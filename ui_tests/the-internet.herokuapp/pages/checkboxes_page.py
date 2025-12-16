from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from retrying import retry
import logging

logger = logging.getLogger(__name__)

class CheckboxesPage:
    """Page Object для страницы checkboxes Elements"""
    
    """Локаторы"""
    CHECKBOX1 = (By.XPATH, "//form[@id='checkboxes']/input[1]")
    CHECKBOX2 = (By.XPATH, "//form[@id='checkboxes']/input[2]")
    CHECKBOXES = (By.XPATH, "//form[@id='checkboxes']/input")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "https://the-internet.herokuapp.com/checkboxes"    
    
    def open(self):
        """Открыть страницу"""
        url = self.url
        self.driver.get(url)
        self._wait_for_page_load()
        logger.info(f"page opened: {url}")
        return self
    
    def _wait_for_page_load(self):
        """Дождаться загрузки страницы"""
        try:
            self.wait.until(EC.presence_of_element_located(self.CHECKBOXES))
        except TimeoutException:
            logger.error("❌ page did not load within the expected time")
            raise
    
    def get_checkboxes_states(self):
        """Получить состояния чекбоксов"""
        checkbox1 = self.driver.find_element(*self.CHECKBOX1)
        checkbox2 = self.driver.find_element(*self.CHECKBOX2)
        assert not checkbox1.is_selected() and checkbox2.is_selected(), "Checkbox states do not match expected defaults"
        return (checkbox1.is_selected(), checkbox2.is_selected())
    
    def toggle_checkbox(self, index):
        """Переключить состояние чекбокса по индексу (0 или 1)"""
        checkbox = self.driver.find_elements(*self.CHECKBOXES)[index]
        checkbox.click()
        assert checkbox.is_selected() != (index == 1)
        return self
    
    def toggle_all_checkboxes(self):
        """Переключить состояние всех чекбоксов"""
        checkboxes = self.driver.find_elements(*self.CHECKBOXES)
        
        for checkbox in checkboxes:
            if not checkbox.is_selected():
                checkbox.click()
        assert all(cb.is_selected() for cb in checkboxes)
        return self
    
    def toggle_none_checkboxes(self):
        """Снять выбор со всех чекбоксов"""
        checkboxes = self.driver.find_elements(*self.CHECKBOXES)
        
        for checkbox in checkboxes:
            if checkbox.is_selected():
                checkbox.click()
        assert all(not cb.is_selected() for cb in checkboxes)
        return self