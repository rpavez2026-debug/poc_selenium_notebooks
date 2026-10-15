from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CartPage(BasePage):
    TITLE = (By.CLASS_NAME, "title")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING = (By.ID, "continue-shopping")

    def wait_until_loaded(self) -> "CartPage":
        self.wait.until(EC.url_contains("cart.html"))
        self.find(self.TITLE)
        return self

    def item_names(self) -> list[str]:
        # find_elements (sin espera) porque el carrito puede estar vacío
        return [e.text for e in self.driver.find_elements(*self.ITEM_NAMES)]

    def item_prices(self) -> list[float]:
        return [self._money(e.text) for e in self.driver.find_elements(*self.ITEM_PRICES)]

    def checkout(self):
        from pages.checkout_pages import CheckoutInfoPage

        self.click(self.CHECKOUT_BUTTON)
        return CheckoutInfoPage(self.driver).wait_until_loaded()
