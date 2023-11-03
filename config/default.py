import os
from logging.config import dictConfig

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "file": {
                "level": "INFO",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": os.path.join(BASE_DIR, "logs/mua.log"),
                "maxBytes": 1024 * 1024 * 5,
                "backupCount": 5,
                "formatter": "default",
            },
        },
        "root": {"level": "INFO", "handlers": ["file"]},
    }
)
