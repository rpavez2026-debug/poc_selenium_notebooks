"""Creación del WebDriver de Chrome, compartida por los tests y los notebooks."""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils.config import env_flag


def create_driver(headless: bool | None = None) -> webdriver.Chrome:
    """Crea un Chrome listo para usar.

    Selenium Manager (incluido en Selenium 4) descarga el chromedriver correcto,
    así que no hay que instalarlo a mano. Si `headless` es None se usa la
    variable de entorno HEADLESS.
    """
    if headless is None:
        headless = env_flag("HEADLESS")

    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1366,900")
    # Evita el popup "cambia tu contraseña" de Chrome (secret_sauce aparece en filtraciones),
    # que bloquea la interacción después del login.
    options.add_argument("--disable-features=PasswordLeakDetection")
    options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        },
    )
    return webdriver.Chrome(options=options)
