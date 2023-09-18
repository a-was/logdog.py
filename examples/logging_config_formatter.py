import logging
import logging.config

logging.config.dictConfig(
    {
        "version": 1,
        "formatters": {
            "json": {
                "()": "logdog.LogfmtFormatter",  # or logdog.JsonFormatter
                "keys": "time level message exception lineno:line filename:file",
                "time_fmt": "iso",
                "include_ms": True,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "json",
                "level": "DEBUG",
            }
        },
        "loggers": {
            "app": {
                "handlers": ["console"],
                "level": "DEBUG",
            }
        },
    }
)

logger = logging.getLogger("app")
logger.info("info")
# time=2023-09-09T14:09:13.837 level=INFO message=info line=32 file=logging_config_formatter.py
# JSON format:
# {"time": "2023-09-09T14:09:13.837", "level": "INFO", "message": "info", "line": 32, "file": "logging_config_formatter.py"}
