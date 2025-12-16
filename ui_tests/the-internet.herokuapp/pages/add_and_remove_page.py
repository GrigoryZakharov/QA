from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from retrying import retry
import logging

logger = logging.getLogger(__name__)

class AddAndRemovePage:
    """Page Object для страницы Add/Remove Elements"""
    
    """Локаторы"""
    ADD_ELEMENT_BUTTON = (By.XPATH, "//button[text()='Add Element']")
    DELETE_BUTTONS = (By.CLASS_NAME, "added-manually")
    PAGE_LOADED_INDICATOR = (By.ID, "content")


    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "https://the-internet.herokuapp.com/add_remove_elements/"
        
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
            self.wait.until(EC.presence_of_element_located(self.PAGE_LOADED_INDICATOR))
            self.wait.until(EC.presence_of_element_located(self.ADD_ELEMENT_BUTTON))
        except TimeoutException:
            logger.error("❌ page did not load within the expected time")
            raise
    
    def add_element(self, count=1):
        """Добавить элементы"""
        for _ in range(count):
            self.driver.find_element(*self.ADD_ELEMENT_BUTTON).click()
        return self
    
    def delete_element(self, index=0):
        """Удалить элемент по индексу"""
        buttons = self.driver.find_elements(*self.DELETE_BUTTONS)
        if index < len(buttons):
            buttons[index].click()
        return self
    
    def delete_all_elements(self):
        """Удалить все элементы"""
        buttons = self.driver.find_elements(*self.DELETE_BUTTONS)
        for button in buttons:
            button.click()
        return self
    
    def get_elements_count(self):
        """Получить количество добавленных элементов"""
        return len(self.driver.find_elements(*self.DELETE_BUTTONS))