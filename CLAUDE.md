# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Proyecto

POC de portafolio: automatización de pruebas UI de https://www.saucedemo.com con Python, Selenium 4, pytest y notebooks de Jupyter, usando Page Object Model. La documentación, los comentarios y los nombres de tests van en español; los identificadores de código, en inglés.

## Comandos (Windows, PowerShell)

```powershell
python -m venv .venv; .venv\Scripts\activate; pip install -r requirements.txt
pytest                                   # suite completa, Chrome visible
pytest --headless                        # sin interfaz (o $env:HEADLESS="1")
pytest -m smoke                          # markers: smoke, regression, known_bug
pytest tests/test_login.py::test_logout_vuelve_al_login   # un solo test
jupyter nbconvert --to notebook --execute --inplace notebooks/01_exploracion_login.ipynb   # ejecutar un notebook sin abrir Jupyter (definir HEADLESS=1 antes)
```

`pytest.ini` siempre genera `reports/report.html` (autocontenido) y define `pythonpath = .`, así que `pages`/`utils` se importan desde la raíz del repo.

## Arquitectura

- `utils/driver_factory.py` → `create_driver()` es el único lugar donde se crea el Chrome, y lo usan tanto los tests como los notebooks. Usa Selenium Manager (no hay que instalar chromedriver) y desactiva el popup de contraseña filtrada de Chrome. Sin eso, el popup bloquea los clics después de iniciar sesión con `secret_sauce`.
- `utils/config.py` tiene `BASE_URL`, la contraseña común `PASSWORD` y el diccionario `USERS` con los usuarios especiales de saucedemo (locked_out, problem, …). Las variables de entorno `BASE_URL`, `DEFAULT_TIMEOUT` y `HEADLESS` reemplazan los valores por defecto.
- `pages/`: `BasePage` encapsula las esperas explícitas con `WebDriverWait` (no se usan esperas implícitas) y el parseo de precios con `_money()`. Los métodos de navegación devuelven el siguiente page object, ya esperado con su `wait_until_loaded()`, así que los flujos se encadenan: `login_as() → InventoryPage → go_to_cart() → CartPage → checkout() → CheckoutInfoPage → continue_to_overview() → CheckoutOverviewPage → finish()`. Los imports entre páginas se hacen dentro de los métodos para evitar imports circulares.
- `LoginPage.login()` solo envía el formulario (sirve para los casos negativos). `login_as()` espera que el login funcione y devuelve `InventoryPage`.
- Los localizadores de las páginas llevan sufijo (`*_INPUT`, `*_BUTTON`) para no tapar constantes importadas: un atributo de clase `PASSWORD` tapaba al `PASSWORD` de `config` en el valor por defecto de `login_as()`.
- `tests/conftest.py`: fixture `driver` con scope de función, más las fixtures `login_page` e `inventory` (sesión iniciada como standard_user). El hook `pytest_runtest_makereport` guarda una captura cuando falla un test y la adjunta al reporte de pytest-html.
- `notebooks/` agregan la raíz del repo a `sys.path` con `Path.cwd().parent`, así que hay que ejecutarlos desde el directorio `notebooks/` (lo normal en Jupyter). En los notebooks se reutilizan los page objects en vez de escribir localizadores sueltos.
- `problem_user` y otros usuarios fallan a propósito. Los tests de esos bugs llevan `@pytest.mark.known_bug` y un `xfail` no estricto.
