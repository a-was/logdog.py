import logging
import logging.config

logging.config.dictConfig(
    {
        "version": 1,
        "formatters": {
            "logfmt": {
                "()": "logdog.LogfmtFormatter",  # or logdog.JsonFormatter
                "keys": "time level message exception lineno:line filename:file",
                "time_fmt": "iso",
                "include_ms": True,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "logfmt",
                "level": "DEBUG",
            },
            "google_chat": {
                "formatter": "logfmt",
                "level": "ERROR",
                "()": "logdog.GoogleChatHandler",
                "webhook_url": "https://...",
            },
            "smtp": {
                "formatter": "logfmt",
                "level": "ERROR",
                "()": "logdog.BufferedSmtpHandler",
                "host": "localhost",
                "port": 25,
                "user": "sender@example.com",
                "password": "password",
                "sender": "Error <sender@example.com>",
                "receivers": ["me@example.com", "you@example.com"],  # or "me@example.com;you@example.com"
                "subject": "Server Error",
                "use_starttls": True,
                "use_ssl": False,
                "capacity": 100,
                "flush_interval": 60 * 15,
                "starting_times": 10,
                "starting_interval": 60,
            },
        },
        "loggers": {
            "app": {
                "handlers": [
                    "console",
                    # "google_chat",
                    # "smtp",
                ],
                "level": "DEBUG",
            },
        },
    }
)

logger = logging.getLogger("app")
logger.info("info")
# time=2023-09-09T14:09:13.837 level=INFO message=info line=32 file=logging_config.py
# JSON format:
# {"time": "2023-09-09T14:09:13.837", "level": "INFO", "message": "info", "line": 32, "file": "logging_config.py"}
