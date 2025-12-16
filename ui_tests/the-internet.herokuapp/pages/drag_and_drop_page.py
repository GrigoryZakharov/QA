from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from retrying import retry
import logging
from selenium.webdriver import ActionChains

logger = logging.getLogger(__name__)

class drag_and_dropPage:
    """Page Object для страницы drag n drop Elements"""

    """Локаторы"""
    BOX_A = By.ID, "column-a"
    BOX_B = By.ID, "column-b"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "https://the-internet.herokuapp.com/drag_and_drop"    
    
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
            self.wait.until(EC.presence_of_element_located(self.BOX_B))
            self.wait.until(EC.presence_of_element_located(self.BOX_A))
        except TimeoutException:
            logger.error(" page did not load within the expected time")
            raise
    
    def drag_and_drop(self, box_from, box_to):
        """"""
        initial_box_from_text = self.driver.find_element(*self.BOX_A).text
        if box_from == "A":
            box_from = self.driver.find_element(*self.BOX_A)
            box_to = self.driver.find_element(*self.BOX_B)
        else:
            box_from = self.driver.find_element(*self.BOX_B)
            box_to = self.driver.find_element(*self.BOX_A)

        drag = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, box_from.get_attribute("id"))))
        drop = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, box_to.get_attribute("id"))))

        action = ActionChains(self.driver).drag_and_drop(drag, drop)
        action.perform()

        current_box_a_text = self.driver.find_element(*self.BOX_A).text

        assert initial_box_from_text != current_box_a_text, "❌ Элементы не были перемещены"
        logger.info("test passed: Elements dragged and dropped successfully")
        return self