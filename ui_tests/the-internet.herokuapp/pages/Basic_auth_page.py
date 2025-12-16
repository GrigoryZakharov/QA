# так и не смог заставить работать, не работает не по alert, не по driver.find_element

from selenium.webdriver.common.by import By

class BasicAuthPage:
    """Page Object для страницы Basic AUth Elements"""
    
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://the-internet.herokuapp.com/basic_auth"
        
    
    def open(self):
        """Открыть страницу"""
        self.driver.get(self.url)
        return self
    
    def login(self, username, password):
        alert = self.driver.switch_to.alert

        alert.send_keys(f"{username}\n{password}")
        alert.accept()
        assert "Congratulations! You must have the proper credentials." in self.driver.page_source
        return self

    def wrong_login(self, username, password):
        alert = self.driver.switch_to.alert

        alert.send_keys(f"{username}\n{password}")
        alert.accept()
        alert.cancel()
        assert "Not authorized" in self.driver.page_source
        return self
    