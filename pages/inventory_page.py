from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class InventoryPage(BasePage):
    TITLE = (By.CLASS_NAME, "title")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    SORT_SELECT = (By.CLASS_NAME, "product_sort_container")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    # Valores del <select> de orden
    SORT_NAME_ASC = "az"
    SORT_NAME_DESC = "za"
    SORT_PRICE_ASC = "lohi"
    SORT_PRICE_DESC = "hilo"

    def wait_until_loaded(self) -> "InventoryPage":
        self.wait.until(EC.url_contains("inventory.html"))
        self.find(self.TITLE)
        return self

    def title(self) -> str:
        return self.text_of(self.TITLE)

    def product_names(self) -> list[str]:
        return [e.text for e in self.find_all(self.ITEM_NAMES)]

    def product_prices(self) -> list[float]:
        return [self._money(e.text) for e in self.find_all(self.ITEM_PRICES)]

    def sort_by(self, value: str) -> "InventoryPage":
        Select(self.find(self.SORT_SELECT)).select_by_value(value)
        return self

    def _product_button(self, product_name: str):
        # Botón "Add to cart"/"Remove" dentro de la tarjeta del producto con ese nombre
        return (
            By.XPATH,
            f"//div[contains(@class,'inventory_item_name') and normalize-space()='{product_name}']"
            "/ancestor::div[contains(@class,'inventory_item_description')]//button",
        )

    def add_to_cart(self, *product_names: str) -> "InventoryPage":
        for name in product_names:
            self.click(self._product_button(name))
        return self

    def remove_from_cart(self, *product_names: str) -> "InventoryPage":
        return self.add_to_cart(*product_names)  # el mismo botón alterna Add/Remove

    def button_text(self, product_name: str) -> str:
        return self.text_of(self._product_button(product_name))

    def cart_count(self) -> int:
        if not self.is_visible(self.CART_BADGE, timeout=1):
            return 0
        return int(self.text_of(self.CART_BADGE))

    def go_to_cart(self):
        from pages.cart_page import CartPage

        self.click(self.CART_LINK)
        return CartPage(self.driver).wait_until_loaded()

    def logout(self):
        from pages.login_page import LoginPage

        self.click(self.MENU_BUTTON)
        self.click(self.LOGOUT_LINK)
        return LoginPage(self.driver)
