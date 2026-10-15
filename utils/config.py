"""Configuración central del POC: ambiente, URL, usuarios de prueba y tiempos de espera."""
import os

# Ambiente donde corre la ejecución (DEV, TEST o PROD). saucedemo.com es el sitio público
# en la web, así que para nosotros es PROD.
AMBIENTES = ("PROD", "TEST", "DEV")
AMBIENTE = os.getenv("AMBIENTE", "PROD").strip().upper()
if AMBIENTE not in AMBIENTES:
    raise ValueError(f"AMBIENTE='{AMBIENTE}' no es válido. Valores permitidos: {', '.join(AMBIENTES)}")
BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com/")
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10"))

# Todos los usuarios de saucedemo comparten la misma contraseña (es pública en el sitio).
PASSWORD = "secret_sauce"

USERS = {
    "standard": "standard_user",
    "locked_out": "locked_out_user",
    "problem": "problem_user",
    "performance_glitch": "performance_glitch_user",
    "error": "error_user",
    "visual": "visual_user",
}


def env_flag(name: str, default: bool = False) -> bool:
    """Lee una variable de entorno booleana (1/true/yes/si)."""
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "si", "sí")
