import logging
import logging.handlers
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "advisor.log"

LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | "
    "%(funcName)s:%(lineno)d | %(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(log_level=logging.INFO):
    """Global logging configuration"""

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Prevent duplicate logs in notebooks / reloads
    if root_logger.handlers:
        return

    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

    # ---- File Handler (advisor.log) ----
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    # ---- Console Handler ----
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


def get_logger(name: str) -> logging.Logger:
    """Get a named logger"""
    return logging.getLogger(name)
