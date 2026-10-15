"""Las tres páginas del checkout: datos del comprador, resumen y confirmación."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CheckoutInfoPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR = (By.CSS_SELECTOR, '[data-test="error"]')

    def wait_until_loaded(self) -> "CheckoutInfoPage":
        self.wait.until(EC.url_contains("checkout-step-one.html"))
        self.find(self.FIRST_NAME)
        return self

    def fill(self, first_name: str, last_name: str, postal_code: str) -> "CheckoutInfoPage":
        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)
        self.type(self.POSTAL_CODE, postal_code)
        self.click(self.CONTINUE_BUTTON)
        return self

    def continue_to_overview(self, first_name: str, last_name: str, postal_code: str):
        self.fill(first_name, last_name, postal_code)
        return CheckoutOverviewPage(self.driver).wait_until_loaded()

    def error_message(self) -> str:
        return self.text_of(self.ERROR)


class CheckoutOverviewPage(BasePage):
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    SUBTOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX = (By.CLASS_NAME, "summary_tax_label")
    TOTAL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")

    def wait_until_loaded(self) -> "CheckoutOverviewPage":
        self.wait.until(EC.url_contains("checkout-step-two.html"))
        self.find(self.TOTAL)
        return self

    def item_names(self) -> list[str]:
        return [e.text for e in self.find_all(self.ITEM_NAMES)]

    def item_prices(self) -> list[float]:
        return [self._money(e.text) for e in self.find_all(self.ITEM_PRICES)]

    def subtotal(self) -> float:
        return self._money(self.text_of(self.SUBTOTAL))

    def tax(self) -> float:
        return self._money(self.text_of(self.TAX))

    def total(self) -> float:
        return self._money(self.text_of(self.TOTAL))

    def finish(self):
        self.click(self.FINISH_BUTTON)
        return CheckoutCompletePage(self.driver).wait_until_loaded()


class CheckoutCompletePage(BasePage):
    HEADER = (By.CLASS_NAME, "complete-header")
    BACK_HOME = (By.ID, "back-to-products")

    def wait_until_loaded(self) -> "CheckoutCompletePage":
        self.wait.until(EC.url_contains("checkout-complete.html"))
        self.find(self.HEADER)
        return self

    def header(self) -> str:
        return self.text_of(self.HEADER)
