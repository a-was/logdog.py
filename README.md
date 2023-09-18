# logdog

Python package with `logging` utilities

This package is grouped into three main functionalities:

- Encoders <br />
They are the "core" of this package.
They are fully functional, but can still be extended and replaced as needed
- Formatters <br />
They allow you to bring structured logging to your app.
Keys present in log lines (such as `time`, `level` or `message`) can be easily configured by using a custom format
- Wrappers <br />
They are just utilities that you can use to simplify the use of logging functions

# Documentation

Documentation is hosted by GitHub Pages - [click here](https://a-was.github.io/logdog.py/)

# Requirements

- Python >= 3.10

# Installation

```bash
pip install -U python-logdog
```

# Usage

> [!NOTE]
> These are only basic examples.
> More advanced ones can be found in [documentation](https://a-was.github.io/logdog.py/)
> and the `examples/` directory

# Wrappers

## LogMessageWrapper

Message wrapper wraps log message (obviously) and adds context to logs <br />
You can specify `prefix` and `suffix` for this values. Default prefix is single space and no suffix

```python
import logging

from logdog import LogMessageWrapper

logging.basicConfig(level=logging.INFO, format="%(asctime)s : %(levelname)-8s : %(message)s")
logger = logging.getLogger("mylogger")

user_id = 1
some_value = "some string"

logger.info("user login", extra={"not": "included", "user": user_id, "value": some_value})
# output: 2023-09-05 12:01:09,836 : INFO     : user login

log = LogMessageWrapper(logger, prefix=" : ")

log.info("user login", user=user_id, action="login", value=some_value)
# output: 2023-09-05 12:01:09,836 : INFO     : user login : user=1 action=login value="some string"
```

## LogExtraWrapper

Extra wrapper wraps `kwargs` into `logging.Record`'s `extra` property <br />
It is recommended to use it together with some formatter

```python
# so this
logger.info("user login", extra={"user": user_id, "value": some_value})

log = LogMessageWrapper(logger)
# is the same as this
log.info("user login", user=user_id, value=some_value)
```

# Formatters

## JsonFormatter

This formatter encodes log as JSON. Internally it uses `JsonEncoder`

```python
import logging

from logdog import JsonFormatter, LogExtraWrapper

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()

formatter = JsonFormatter()  # no arguments -> using default format
handler.setFormatter(formatter)

# without wrapper
user_id = 1
logger.info("user login", extra={"user": user_id, "action": "login"})
# output: {"time": "2023-09-09 13:39:31,191", "level": "INFO", "message": "user login", "user": 1, "action": "login"}

# with wrapper - optional but recommended
log = LogExtraWrapper(logger)

user_id = 2
log.info("user login", user=user_id, action="login")
# output: {"time": "2023-09-09 13:39:31,191", "level": "INFO", "message": "user login", "user": 2, "action": "login"}
```

## LogfmtFormatter

This formatter encodes log with logfmt format. Internally it uses `LogfmtEncoder`

```python
import logging

from logdog import LogExtraWrapper, LogfmtFormatter

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()

formatter = LogfmtFormatter(
    "time:ts level:at message:msg exception:exc filename:file lineno:line",
    time_fmt="iso",
)
handler.setFormatter(formatter)

log = LogExtraWrapper(logger)

user_id = 12
action = "login"
log.info("user performed action", user=user_id, action=action)
# output:
# ts=2023-09-09T13:39:31,191 at=INFO msg="user performed action" file=login.py line=75 user=12 action=login
```

## File config

Check the `examples/logging_config_formatter.py` file

TL;DR
```python
{
    "formatters": {
        "logfmt": {
            "()": "logdog.LogfmtFormatter",  # or logdog.JsonFormatter
            "keys": "time level message exception lineno:line filename:file",  # optional
            "time_fmt": "default",  # optional
            "include_ms": True,  # optional
        },
    },
}
```
