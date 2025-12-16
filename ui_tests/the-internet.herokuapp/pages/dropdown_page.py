from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from retrying import retry
import logging

logger = logging.getLogger(__name__)

class DrownPage:
    """Page Object для страницы drag n drop Elements"""
    '''Локаторы'''
    DROPDOWN = (By.ID, "dropdown")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "https://the-internet.herokuapp.com/dropdown"    
    
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
            self.wait.until(EC.presence_of_element_located(self.DROPDOWN))
        except TimeoutException:
            logger.error("❌ page did not load within the expected time")
            raise
    
    def get_dropdown_state(self):
        """"""
        iniitial_state = self.driver.find_element(*self.DROPDOWN).get_attribute("value")
        assert iniitial_state == "", "❌ Начальное состояние дропдауна неверно"
        return iniitial_state
    
    def select_option(self, option_value):
        """"""
        dropdown = self.driver.find_element(*self.DROPDOWN)
        dropdown.find_element(By.XPATH, f"//option[@value='{option_value}']").click()
        selected_value = dropdown.get_attribute("value")
        assert selected_value == option_value, "❌ Опция дропдауна не была выбрана"
        return self