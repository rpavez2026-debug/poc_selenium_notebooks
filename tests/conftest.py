import base64
from pathlib import Path

import pytest

from pages import LoginPage
from utils.config import USERS
from utils.driver_factory import create_driver

SCREENSHOTS_DIR = Path(__file__).resolve().parent.parent / "reports" / "screenshots"


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Ejecuta Chrome sin interfaz (también se puede usar HEADLESS=1)",
    )


@pytest.fixture
def driver(request):
    headless = True if request.config.getoption("--headless") else None
    drv = create_driver(headless=headless)
    yield drv
    drv.quit()


@pytest.fixture
def login_page(driver) -> LoginPage:
    return LoginPage(driver).load()


@pytest.fixture
def inventory(login_page):
    """Sesión iniciada con standard_user, parada en la página de productos."""
    return login_page.login_as(USERS["standard"])


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Si un test falla, guarda captura de pantalla y la adjunta al reporte HTML."""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return
    drv = item.funcargs.get("driver")
    if drv is None:
        return

    png = drv.get_screenshot_as_png()
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in item.nodeid)
    (SCREENSHOTS_DIR / f"{safe_name}.png").write_bytes(png)

    pytest_html = item.config.pluginmanager.getplugin("html")
    if pytest_html is not None:
        extras = getattr(report, "extras", [])
        extras.append(pytest_html.extras.image(base64.b64encode(png).decode(), mime_type="image/png"))
        report.extras = extras
