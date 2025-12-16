from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from retrying import retry
import logging

logger = logging.getLogger(__name__)

class BrokenImgPage:
    """Page Object для страницы BrokenImg Elements"""
    
    IMAGES = (By.TAG_NAME, "img")

    def __init__(self, driver):
        self.driver = driver
        self.url = "https://the-internet.herokuapp.com/broken_images"
    
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
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(self.IMAGES)
            )
        except TimeoutException:
            logger.error("❌ page did not load within the expected time")
            raise

    def get_total_images_count(self):
        """Получить общее количество изображений на странице"""
        images = self.driver.find_elements(*self.IMAGES)
        count = len(images)
        logger.info(f"Total images found: {count}")
        return count

    def check_images(self):
        """Проверить наличие сломанных изображений на странице"""
        images = self.driver.find_elements(*self.IMAGES) 
        broken_images = []
        for img in images:
            natural_width = self.driver.execute_script(
                "return arguments[0].naturalWidth", img
            )
        
            if natural_width == 0:
                broken_images.append({
                    'src': img.get_attribute('src'),
                    'alt': img.get_attribute('alt'),
                    'width': natural_width
                })
        logger.info(f"Broken images found: {len(broken_images)}")
        print(broken_images)
        
        assert len(broken_images) > 0, f"Нет сломанных изображений на странице"
        return broken_images