from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    # Lokatory elementów na stronie
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "doLogin")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".alert-danger")

    def login_to_admin_panel(self, username: str, password: str):
        self.send_keys(self.USERNAME_INPUT, username)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message_text(self) -> str:
        return self.find_element(self.ERROR_MESSAGE).text