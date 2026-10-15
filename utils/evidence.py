"""Capturas de pantalla como evidencia de ejecución."""
from datetime import datetime
from pathlib import Path

from utils.logger import get_logger

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EVIDENCE_DIR = PROJECT_ROOT / "reports" / "evidencias"


def save_screenshot(driver, name: str) -> Path:
    """Guarda una captura en reports/evidencias/ y deja la ruta en el log."""
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    path = EVIDENCE_DIR / f"{name}_{datetime.now():%d-%m-%Y_%H%M%S}.png"
    driver.save_screenshot(str(path))
    get_logger().info("Captura guardada: %s", path.relative_to(PROJECT_ROOT))
    return path
