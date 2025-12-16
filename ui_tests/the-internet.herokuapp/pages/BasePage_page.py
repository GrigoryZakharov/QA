class BasePage:
    """Базовый класс для всех страниц"""
    
    def __init__(self, driver):
        self.driver = driver
    
    def open(self, url):
        """Открыть страницу по URL"""
        self.driver.get(url)
        return self

    def refresh(self):
        """Обновить страницу"""
        self.driver.refresh()
        return self
