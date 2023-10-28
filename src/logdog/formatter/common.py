import enum
import re


class TimeFormat(enum.Enum):
    DEFAULT = "default"
    ISO = "iso"
    ISO_TIMEZONE = "iso_tz"
    TIMESTAMP = "timestamp"
    TIMESTAMP_FLOAT = "timestamp_float"
    TIMESTAMP_MILLISECONDS = "timestamp_ms"
    TIMESTAMP_MICROSECONDS = "timestamp_us"
    TIMESTAMP_NANOSECONDS = "timestamp_ns"


re_fmt = re.compile(r"([a-zA-Z]+)(?::([a-zA-Z-._]+))?")
supported_keys = (
    "time",
    "level",
    "levelno",
    "message",
    "exception",
    "logger",
    "filename",
    "funcName",
    "lineno",
    "module",
    "pathname",
    "process",
    "processName",
    "thread",
    "threadName",
    "taskName",
)
supported_since_python_version = {
    "taskName": (3, 12),
}

standard_logging_record_attrs = frozenset(
    (
        "args",
        "asctime",
        "created",
        "exc_info",
        "exc_text",
        "filename",
        "funcName",
        "levelname",
        "levelno",
        "lineno",
        "module",
        "msecs",
        "message",
        "msg",
        "name",
        "pathname",
        "process",
        "processName",
        "relativeCreated",
        "stack_info",
        "taskName",
        "thread",
        "threadName",
    )
)
