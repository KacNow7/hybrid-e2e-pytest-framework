import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver(request):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    # Inicjalizacja przeglądarki
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    
    yield driver
    
    # Przechwycenie błędu i zrobienie zrzutu ekranu
    if request.node.rep_call.failed:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Screenshot_on_failure",
            attachment_type=allure.attachment_type.PNG
        )
    
    driver.quit()

# Hook pytest do monitorowania statusu testu
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)