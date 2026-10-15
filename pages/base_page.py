"""Clase base de los Page Objects: esperas explícitas y acciones comunes."""
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config import BASE_URL, DEFAULT_TIMEOUT
from utils.logger import get_logger

log = get_logger()


class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def open(self, path: str = ""):
        log.info("Navegando a %s", BASE_URL + path)
        self.driver.get(BASE_URL + path)

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        """Espera a que exista al menos un elemento y devuelve todos."""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text: str):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def text_of(self, locator) -> str:
        return self.find(locator).text

    def texts_of(self, locator, attempts: int = 3) -> list[str]:
        """Texto de todos los elementos, sin esperar (la lista puede estar vacía).

        Si la página vuelve a dibujar la lista mientras se lee, los elementos quedan obsoletos
        (StaleElementReferenceException): se buscan de nuevo hasta `attempts` veces.
        """
        for attempt in range(1, attempts + 1):
            try:
                return [e.text for e in self.driver.find_elements(*locator)]
            except StaleElementReferenceException:
                if attempt == attempts:
                    raise
                log.info("Elementos obsoletos en %s, reintentando (%d/%d)", locator, attempt, attempts)

    def is_visible(self, locator, timeout: float = 2) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    def screenshot_png(self) -> bytes:
        return self.driver.get_screenshot_as_png()

    @staticmethod
    def _money(text: str) -> float:
        """Convierte '$29.99' o 'Total: $32.39' en 29.99 / 32.39."""
        return float(text.split("$")[-1])
