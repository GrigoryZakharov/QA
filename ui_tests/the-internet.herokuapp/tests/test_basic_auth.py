'''
from pages.Basic_auth_page import BasicAuthPage

def test_correct_login(clean_browser):
    """Тест добавления одного элемента"""
    page = BasicAuthPage(clean_browser)
    page.open().login("admin", "admin")

    print("✅ Успешный вход выполнен")

def test_incorrect_login(clean_browser):
    """Тест добавления одного элемента"""
    page = BasicAuthPage(clean_browser)
    page.open()
    
    try:
        page.wrong_login("wrong_user", "wrong_pass")
    except AssertionError:
        print("✅ Некорректный вход обработан правильно")
    else:
        raise AssertionError("❌ Некорректный вход не был обработан")
'''