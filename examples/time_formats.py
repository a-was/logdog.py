import logging

from src.logdog.formatter import JsonFormatter, TimeFormat

# logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

logger.addHandler(handler)

"""
Supported time formats:

TimeFormat.DEFAULT / "default"
"2023-09-09 13:34:58.149"

TimeFormat.ISO / "iso"
"2023-09-09T13:34:58"

TimeFormat.ISO_TIMEZONE / "iso_tz"
"2023-09-09T13:34:58.150+02:00"

TimeFormat.TIMESTAMP / "timestamp"
1694259298

TimeFormat.TIMESTAMP_FLOAT / "timestamp_float"
1694259298.150456

TimeFormat.TIMESTAMP_MILLISECONDS / "timestamp_ms"
1694259298150

TimeFormat.TIMESTAMP_MICROSECONDS / "timestamp_us"
1694259298150456

TimeFormat.TIMESTAMP_NANOSECONDS / "timestamp_ns"
1694259298150456064
"""

formatter = JsonFormatter()
handler.setFormatter(formatter)
logger.info("default")
# {"time": "2023-09-09 13:34:58,149", "level": "INFO", "message": "default"}

formatter = JsonFormatter(
    time_fmt=TimeFormat.ISO,  # use Enum
    # time_fmt="iso",  # or string
    include_ms=False,  # setting this to false will prevent appending ms at the end of time string (".123")
)
handler.setFormatter(formatter)
logger.info("style 2")
# {"time": "2023-09-09T13:34:58", "level": "INFO", "message": "style 2"}


# https://docs.python.org/3/library/time.html#time.strftime
formatter = JsonFormatter(
    time_fmt="custom:%a, %d %b %Y %H:%M:%S %z",
    include_ms=False,
)
handler.setFormatter(formatter)
logger.info("custom")
# {"time": "custom:Sat, 09 Sep 2023 13:34:58 +0200", "level": "INFO", "message": "custom"}
