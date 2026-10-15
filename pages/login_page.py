from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config import PASSWORD


class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR = (By.CSS_SELECTOR, '[data-test="error"]')

    def load(self) -> "LoginPage":
        self.open()
        self.find(self.LOGIN_BUTTON)
        return self

    def login(self, username: str, password: str):
        """Llena el formulario y envía. No asume que el login sea exitoso."""
        self.type(self.USERNAME_INPUT, username)
        self.type(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def login_as(self, username: str, password: str = PASSWORD):
        """Login esperado como exitoso: devuelve la página de productos."""
        from pages.inventory_page import InventoryPage

        self.login(username, password)
        return InventoryPage(self.driver).wait_until_loaded()

    def error_message(self) -> str:
        return self.text_of(self.ERROR)

    def is_displayed(self) -> bool:
        return self.is_visible(self.LOGIN_BUTTON)
