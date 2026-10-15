"""Log de ejecución: cada línea lleva fecha dd-mm-aaaa, hora y el ambiente (DEV/TEST/PROD)."""
import logging
import sys
from datetime import datetime
from pathlib import Path

from utils.config import AMBIENTE

LOGGER_NAME = "poc"
LOG_FORMAT = "%(asctime)s | %(ambiente)s | %(levelname)-7s | %(message)s"
DATE_FORMAT = "%d-%m-%Y %H:%M:%S"
LOGS_DIR = Path(__file__).resolve().parent.parent / "reports" / "logs"


class _AmbienteFilter(logging.Filter):
    """Agrega el ambiente a cada registro para poder usarlo en el formato."""

    def filter(self, record):
        record.ambiente = AMBIENTE
        return True


_logger = logging.getLogger(LOGGER_NAME)
_logger.setLevel(logging.INFO)
_logger.addFilter(_AmbienteFilter())


def get_logger() -> logging.Logger:
    """Logger único del proyecto (lo usan los page objects y los notebooks)."""
    return _logger


def setup_execution_log(execution_name: str) -> Path:
    """Muestra el log en pantalla y lo guarda en reports/logs/. Devuelve la ruta del archivo.

    Se puede llamar varias veces (por ejemplo al re-ejecutar una celda): reemplaza los
    handlers anteriores en vez de duplicar las líneas.
    """
    for handler in list(_logger.handlers):
        _logger.removeHandler(handler)
        handler.close()

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOGS_DIR / f"{execution_name}_{datetime.now():%d-%m-%Y_%H%M%S}.log"
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    for handler in (logging.StreamHandler(sys.stdout), logging.FileHandler(log_file, encoding="utf-8")):
        handler.setFormatter(formatter)
        _logger.addHandler(handler)
    _logger.propagate = False
    return log_file
