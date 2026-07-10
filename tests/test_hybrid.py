import requests
from pages.login_page import LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_invalid_login_behavior_on_ui(driver):
    # Krok 1: Wejście na stronę główną (zamiast wymuszania /#/admin)
    driver.get("https://automationintesting.online/")
    
    # Krok 2: Kliknięcie w przycisk "Admin" w nawigacji, tak jak zrobiłby to człowiek
    wait = WebDriverWait(driver, 10)
    admin_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Admin")))
    admin_link.click()
    
    # Krok 3: Inicjalizacja strony logowania
    login_page = LoginPage(driver)
    
    # Krok 4: Egzekucja scenariusza negatywnego
    login_page.login_to_admin_panel("wrong_user", "invalid_password")
    
    # Krok 5: Weryfikacja obecności komunikatu o błędzie
    error_text = login_page.get_error_message_text()
    assert "Invalid credentials" in error_text

def test_api_health_check_before_ui_interaction():
    response = requests.get("https://restful-booker.herokuapp.com/ping")
    assert response.status_code == 201