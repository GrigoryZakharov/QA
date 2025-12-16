import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import logging
from datetime import datetime
from pages.dynamic_content_page import DynamicContentPage
from pages.add_and_remove_page import AddAndRemovePage
from pages.broken_img_page import BrokenImgPage
from pages.checkboxes_page import CheckboxesPage
from pages.context_menu_page import context_menuPage
from pages.drag_and_drop_page import drag_and_dropPage
from pages.dropdown_page import DrownPage
import os

def pytest_configure(config):
    """Настройка логирования для всех тестов"""
    log_dir = "logs"  # Относительный путь
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )


@pytest.fixture(scope = "session")
def browser():
    # Настройки Chrome
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    
    # Скрываем сообщение "Chrome is being controlled by automated test software"
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Автоматическая установка драйвера
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Настройки
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    driver.set_window_size(1920, 1080)
    
    yield driver
    
    driver.quit()

@pytest.fixture()
def clean_browser(browser):
    browser.delete_all_cookies()
    
    # Переходим на пустую страницу
    browser.get("about:blank")
    
    yield browser

@pytest.fixture()
def add_and_remove_page(clean_browser):
    page = AddAndRemovePage(clean_browser)
    yield page

@pytest.fixture()
def dynamic_content_page(clean_browser):
    page = DynamicContentPage(clean_browser)
    yield page

@pytest.fixture()
def broken_img_page(clean_browser):
    page = BrokenImgPage(clean_browser)
    yield page

@pytest.fixture()
def check_box_page(clean_browser):
    page = CheckboxesPage(clean_browser)
    yield page

@pytest.fixture()
def context_menu_page(clean_browser):
    page = context_menuPage(clean_browser)
    yield page

@pytest.fixture()
def drag_and_drop_page(clean_browser):
    page = drag_and_dropPage(clean_browser)
    yield page

@pytest.fixture()
def dropdown_page(clean_browser):
    page = DrownPage(clean_browser)
    yield page