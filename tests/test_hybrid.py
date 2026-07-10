import pytest
from pages.login_page import LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.parametrize("username, password", [
    ("wrong_user", "invalid_password"),
    ("admin", "wrong_pass123")
])
def test_invalid_login_behavior_on_ui(driver, base_url, username, password):
    driver.get(base_url)
    
    wait = WebDriverWait(driver, 10)
    admin_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Admin")))
    admin_link.click()
    
    login_page = LoginPage(driver)
    login_page.login_to_admin_panel(username, password)
    
    error_text = login_page.get_error_message_text()
    assert "Invalid credentials" in error_text