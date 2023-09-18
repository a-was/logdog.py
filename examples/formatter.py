import logging

from src.logdog import JsonFormatter, LogExtraWrapper, LogfmtFormatter

# try to change formatter
# FormatterClass = JsonFormatter
FormatterClass = LogfmtFormatter


# logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

logger.addHandler(handler)

formatter = FormatterClass()
handler.setFormatter(formatter)

logger.info("custom formatters")
# {"time": "2023-09-09 13:18:47,731", "level": "INFO", "message": "custom formatters"}
# time="2023-09-09 13:18:47,731" level=INFO message="custom formatters"

# without wrapper
logger.info("Without wrapper", extra={"key": "value"})
# {"time": "2023-09-09 13:18:47,731", "level": "INFO", "message": "Without wrapper", "key": "value"}
# time="2023-09-09 13:18:47,731" level=INFO message="Without wrapper" key=value

# with wrapper
log = LogExtraWrapper(logger)

log.logger.info("You can access logger")
# {"time": "2023-09-09 13:19:32,835", "level": "INFO", "message": "You can access logger"}
log.logger.info("Logger with extra", extra={"key": "value"})
# {"time": "2023-09-09 13:19:32,835", "level": "INFO", "message": "Logger with extra", "key": "value"}
# time="2023-09-09 13:19:32,835" level=INFO message="Logger with extra" key=value
log.info("Message without kwargs")
# {"time": "2023-09-09 13:19:32,835", "level": "INFO", "message": "Message without kwargs"}
log.info("Message with kwargs", key="value", user_id=2)
# {"time": "2023-09-09 13:19:32,835", "level": "INFO", "message": "Message with kwargs", "key": "value", "user_id": 2}
# time="2023-09-09 13:19:32,835" level=INFO message="Message with kwargs" key=value user_id=2


# exception
try:
    1 / 0
except ZeroDivisionError:
    log.exception("exception message", key="value")
# {"time": "2023-09-09 13:39:31,191", "level": "ERROR", "message": "exception message",
# "exception": ["Traceback (most recent call last):", "File \".../examples/formatter.py\", line 47, in <module>", "1 / 0", "ZeroDivisionError: division by zero"],
# "key": "value"}

# time="2023-09-09 13:39:31,191" level=ERROR message="exception message"
# exception=["Traceback (most recent call last):" "File \".../examples/formatter.py\", line 47, in <module>" "1 / 0" "ZeroDivisionError: division by zero"]
# key=value


# custom types setup
from datetime import date, datetime, timezone
from enum import Enum


class LanguageEnum(Enum):
    ENGLISH = "en"


language = LanguageEnum.ENGLISH

today = date.today()
now = datetime.now()
now_tz = datetime.now(tz=timezone.utc)

# custom types usage
log.info(
    "custom types",
    language=language,
    language_value=language.value,
    today=today,
    now=now,
    now_tz=now_tz,
)
# {"time": "2023-09-09 13:39:31,191", "level": "INFO", "message": "custom types", "language": "ENGLISH", "language_value": "en", "today": "2023-09-09", "now_tz": "2023-09-09T11:39:31.191997+00:00", "now": "2023-09-09T13:39:31.191997"}
# time="2023-09-09 13:39:31,191" level=INFO message="custom types" language=ENGLISH language_value=en today=2023-09-09 now_tz=2023-09-09T11:39:31.191997+00:00  now=2023-09-09T13:39:31.191997

# custom formats:

formatter = FormatterClass(
    "time:ts level:lvl message:msg exception:exc",
    time_fmt="iso_tz",
)
handler.setFormatter(formatter)
log.error("Some error", key="value", user_id=2)
# {"ts": "2023-09-09T13:39:31.193+02:00", "lvl": "ERROR", "msg": "Some error", "key": "value", "user_id": 2}
# ts=2023-09-09T13:39:31.193+02:00 lvl=ERROR msg="Some error" user_id=2 key=value

formatter = FormatterClass("time:ts level:- levelno:at message:msg", time_fmt="iso_tz")
handler.setFormatter(formatter)
log.info("info")
# {"ts": "2023-09-09T13:44:03.335+02:00", "msg": "info", "at": 20}
# ts=2023-09-09T13:44:03.335+02:00 msg=info at=20

# all attributes
formatter = FormatterClass(
    "time level message exception levelno logger filename funcName lineno module pathname process processName thread threadName"
)
handler.setFormatter(formatter)
log.info("info")
# {"time": "2023-09-09 13:45:22,133", "level": "INFO", "message": "info",
# "levelno": 20, "logger": "__main__", "filename": "formatter.py", "funcName": "<module>", "lineno": 111,
# "module": "formatter", "pathname": ".../examples/formatter.py",
# "process": 6304, "processName": "MainProcess", "thread": 11072, "threadName": "MainThread"}

# time="2023-09-09 13:45:22,133" level=INFO message=info levelno=20 logger=__main__
# filename=formatter.py funcName=<module> lineno=111 module=formatter pathname=.../examples/formatter.py
# process=6304 processName=MainProcess thread=11072 threadName=MainThread
