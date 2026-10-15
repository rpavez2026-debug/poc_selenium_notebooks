# POC Selenium + Notebooks · saucedemo.com

Prueba de concepto de automatización web sobre [saucedemo.com](https://www.saucedemo.com) usando
**Python + Selenium 4 + pytest**, con el patrón **Page Object Model**, y notebooks de **Jupyter**
para explorar los flujos paso a paso con capturas de pantalla.

## Qué cubre

| Área | Casos |
|---|---|
| Login | login exitoso, usuario bloqueado, password incorrecta, campos vacíos, logout, acceso sin sesión |
| Catálogo | 6 productos, ordenamiento (nombre A-Z/Z-A, precio asc/desc), agregar/quitar del carrito |
| Checkout | compra end-to-end con validación de subtotal/impuesto/total, campos obligatorios |
| Bugs conocidos | `problem_user` con ordenamiento roto (marcado `xfail`) |

## Requisitos

- Python 3.11+
- Google Chrome (Selenium Manager descarga el chromedriver automáticamente)

## Instalación

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecutar los tests

```powershell
pytest                                  # suite completa, Chrome visible
pytest --headless                       # sin interfaz (o $env:HEADLESS="1")
pytest -m smoke                         # solo pruebas críticas
pytest tests/test_checkout.py           # un archivo
pytest -k "compra_completa"             # un test por nombre
```

Se genera un reporte en `reports/report.html`. Si un test falla, la captura de pantalla
queda adjunta en el reporte y guardada en `reports/screenshots/`.

## Notebooks

```powershell
jupyter notebook notebooks/
```

- `01_exploracion_login.ipynb`: casos positivos y negativos del login.
- `02_login_con_falla.ipynb`: login con `locked_out_user`; termina en `[FALLO]` porque saucedemo bloquea a ese usuario.
- `03_flujo_compra_e2e.ipynb`: compra completa validando montos.
- `04_flujo_problem_user.ipynb`: catálogo, carrito y checkout con `problem_user`; deja en `[FALLO]` sus bugs (imágenes, orden, carrito, formulario).

Cada notebook tiene **una sola celda de código**. Al ejecutarla, debajo aparece el log de lo que
va haciendo, con fecha `dd-mm-aaaa`, hora y ambiente:

```
14-10-2026 23:55:48 | PROD | INFO    | Agregando al carrito: Sauce Labs Backpack
14-10-2026 23:55:49 | PROD | INFO    | [OK] Montos del resumen correctos
```

El log también se guarda en un archivo por ambiente y por día, y las capturas en `reports/evidencias/`:

```
reports/logs/
└── PROD/              (o TEST / DEV)
    └── 2026/10/15/
        ├── 01_exploracion_login.log
        ├── 02_login_con_falla.log
        ├── 03_flujo_compra_e2e.log
        └── 04_flujo_problem_user.log
```

Las ejecuciones del mismo día se agregan al final del mismo archivo, cada una entre sus líneas `INICIO` y `FIN`.

## Ambientes

La variable `AMBIENTE` (`PROD`, `TEST` o `DEV`; cualquier otro valor da error) indica dónde corre la ejecución y aparece en el
log y en el reporte HTML. Por defecto es `PROD`, porque saucedemo.com es el sitio público.
Para apuntar a otro ambiente:

```powershell
$env:AMBIENTE="TEST"; $env:BASE_URL="https://url-de-test/"; pytest
```

## Estructura

```
pages/      Page Objects (una clase por pantalla, esperas explícitas en BasePage)
tests/      Tests pytest + conftest (fixtures del driver y capturas en fallos)
notebooks/  Ejecuciones de una sola celda con log por ambiente, reutilizando los Page Objects
utils/      Configuración (ambiente, URL, usuarios), driver de Chrome, log y evidencias
```
