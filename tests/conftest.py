import pytest
import allure
import os
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

load_dotenv()

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="qa", help="Environment to run tests against")

@pytest.fixture(scope="session")
def base_url(request):
    return os.getenv("UI_BASE_URL")

@pytest.fixture
def driver(request):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    # Przełącznik środowiska (Lokalnie vs Docker)
    execution_env = os.getenv("EXECUTION_ENV")
    
    if execution_env == "docker":
        # Łączymy się z kontenerem Selenium (Remote WebDriver)
        selenium_host = os.getenv("SELENIUM_HOST", "localhost")
        driver = webdriver.Remote(
            command_executor=f"http://{selenium_host}:4444/wd/hub",
            options=options
        )
    else:
        # Standardowe uruchomienie lokalne
        driver = webdriver.Chrome(options=options)
        
    driver.implicitly_wait(5)
    
    yield driver
    
    # Robienie zrzutu ekranu w przypadku błędu
    if request.node.rep_call.failed:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Screenshot_on_failure",
            attachment_type=allure.attachment_type.PNG
        )
    
    driver.quit()

@pytest.fixture
def create_test_booking():
    api_url = os.getenv("API_BASE_URL")
    payload = {
        "firstname": "Test", "lastname": "User", "totalprice": 100,
        "depositpaid": True, "bookingdates": {"checkin": "2026-10-01", "checkout": "2026-10-10"}
    }
    
    # Setup: Utworzenie rezerwacji
    response = requests.post(f"{api_url}/booking", json=payload)
    booking_id = response.json().get("bookingid")
    
    # Przekazanie ID do testu
    yield booking_id
    
    print(f"\nTeardown: Usunięto rezerwację ID {booking_id}")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)