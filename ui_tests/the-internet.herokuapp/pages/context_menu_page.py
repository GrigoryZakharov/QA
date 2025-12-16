from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from retrying import retry
from selenium.webdriver import ActionChains
import logging

logger = logging.getLogger(__name__)

class context_menuPage:
    """Page Object для страницы ContextMenu Elements"""
    
    """Локаторы"""
    BOX = (By.ID, "hot-spot")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "https://the-internet.herokuapp.com/context_menu"    
    
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
            self.wait.until(EC.presence_of_element_located(self.BOX))
        except TimeoutException:
            logger.error("❌ page did not load within the expected time")
            raise
    
    
    def right_click_box(self):
        """Кликнуть правой кнопкой мыши на квадрате"""
        box = self.driver.find_element(*self.BOX)
        action = ActionChains(self.driver)
        action.context_click(box).perform()
        alert = self.driver.switch_to.alert
        alert_text = alert.text
        alert.accept()
        assert alert_text == "You selected a context menu"
        import time
        time.sleep(0.5)  # Небольшая пауза чтобы алерт успел закрыться
        try:
            # Кликаем в правый нижний угол (относительно viewport)
            ActionChains(self.driver).move_by_offset(100, 100).click().perform()
        except Exception as e:
            logger.error(f"❌ Failed to click outside context menu: {e}")
            raise

        return self
    