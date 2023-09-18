# Formatters

Formatters lets you bring structured logging to your app

## Keys format

Firstly, you define which fields you want to include in logs

### Supported keys

{==

**time**, **level**, **message**, **exception**, logger, levelno, filename,
funcName, lineno, module, pathname, process, processName, thread, threadName

==}

You add, create an alias or remove them to log output by passing string in special format to Formatter you want to use

### Some quick format examples

- `"time level message exception"`
- `"logger"`
- `"time:ts level:at message:msg exception:exc"`
- `"level:- levelno:level"`
- `"filename:file lineno:line funcName:fn"`

Bolded keys are default, so `time`, `level`, `message` and `exception` are special -
**they are always included in format - unless explicitly disabled** (e.g. `level:-`)

So the format `"logger"` is equivalent to format `"time level message exception logger"`.
Same as `"time logger"`, `"time level logger"` etc.

Aliases (`time:ts filename:file`) work as you would expect,
so the output log will have the time under `ts` key and file name under the `file` key

**The `exception` key is only present when using the `logger.exception` method**
(or by setting the `exc_info` argument to `logger` methods).
Exception string is formatted as list of strings.
Exception example can be found in `examples/formatter.py` file

### More examples

- `filename lineno:line funcName:func` <br />
This extends the default fields (so `time`, `level`, `message` and `exception` will be present)
and adds three more keys - `filename`, `line` and `func`

- `time:ts level:lvl message:msg exception:exc lineno:line funcName:func` <br />
This renames the default fields and adds two more

- `time:ts level:- levelno:level` <br />
This renames the `time` key to `ts`, disables default `level` key and adds the `levelno` key under `level` alias

- `time level message exception logger levelno filename funcName lineno module pathname process processName thread threadName` <br />
This enables all the keys

So you can add new fields by separating them with spaces,
create an alias for each key and disable default ones with special `-` value

**Extra keys are always added, so they are not included in this format**


## JsonFormatter

This formatter encodes log as JSON. Internally it uses `JsonEncoder`

I recommend to use it with `LogExtraWrapper` so you don't have to use `extra={...}` keyword in logger. Just use `kwargs`

```python
import logging

from logdog import JsonFormatter, LogExtraWrapper

# logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)

formatter = JsonFormatter()  # no arguments -> using default format
handler.setFormatter(formatter)

log = LogExtraWrapper(logger)  # optional but recommended

user_id = 12
action = "login"
log.info("user performed action", user=user_id, action=action)
# output:
# {"time": "2023-09-09 13:39:31,191", "level": "INFO", "message": "user performed action", "user": 12, "action": "login"}
```


## LogfmtFormatter

This formatter encodes log with logfmt format. Internally it uses `LogfmtEncoder` so all the formatting is done by it

I recommend to use it with `LogExtraWrapper` so you don't have to use `extra={...}` keyword in logger. Just use `kwargs`

```python
import logging

from logdog import LogExtraWrapper, LogfmtFormatter

# logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)

formatter = LogfmtFormatter(
    "time:ts level:at message:msg exception:exc filename:file lineno:line",
    time_fmt="iso",
)
handler.setFormatter(formatter)

log = LogExtraWrapper(logger)  # optional but recommended

user_id = 12
action = "login"
log.info("user performed action", user=user_id, action=action)
# output:
# ts=2023-09-09T13:39:31,191 at=INFO msg="user performed action" file=login.py line=75 user=12 action=login
```


## Time formats

Serval time formats are supported. Use `time_fmt` argument to formatter to set one.
It can be either string or `logdog.formatter.TimeFormat` enum type

### Supported time formats

- `TimeFormat.DEFAULT` or `"default"` <br />
output: `2023-09-09 13:34:58,149`

- `TimeFormat.ISO` or `"iso"` <br />
output: `2023-09-09T13:34:58.149`

- `TimeFormat.ISO_TIMEZONE` or `"iso_tz"` <br />
output: `2023-09-09T13:34:58.150+02:00`

- `TimeFormat.TIMESTAMP` or `"timestamp"` <br />
output: `1694259298`

- `TimeFormat.TIMESTAMP_FLOAT` or `"timestamp_float"` <br />
output: `1694259298.150456`

- `TimeFormat.TIMESTAMP_MILLISECONDS` or `"timestamp_ms"` <br />
output: `1694259298150`

- `TimeFormat.TIMESTAMP_MICROSECONDS` or `"timestamp_us"` <br />
output: `1694259298150456`

- `TimeFormat.TIMESTAMP_NANOSECONDS` or `"timestamp_ns"` <br />
output: `1694259298150456064`

- custom, for example `custom:%a, %d %b %Y %H:%M:%S %z` <br />
output: `custom:Sat, 09 Sep 2023 13:34:58 +0200`

Check the `examples/time_formats.py` file for usage examples


## Milliseconds

For the `default` and `iso` formats an `include_ms` argument of type bool is respected. It is `True` by default.
For `default` format it appends `,xxx` to time string and for `iso` format is uses dot notation so it appends `.xxx`


## File config

Using dict config

```python
{
    "formatters": {
        "json": {
            "()": "logdog.LogfmtFormatter",  # or logdog.JsonFormatter
            "keys": "time level message exception lineno:line filename:file",  # optional
            "time_fmt": "iso",  # optional
            "include_ms": True,  # optional
        },
    },
}
```


## Writing your own formatter

You can create your own formatter, for example to use your custom encoder

```python
from logdog.formatter import BaseFormatter

class MyFormatter(BaseFormatter):
    _encoder = MyEncoder()

    def _format_out_dict(self, out: dict[str, Any]) -> str:
        return self._encoder.encode(out)
```


## Formatter *middleware*

You can also extend existing formatters. It allows you to create some kind of logging middleware

For example, to add `"AUDIT:"` prefix to every log message you can do this

```python
from logdog.formatter import JsonFormatter

class AuditJsonFormatter(JsonFormatter):
    def _format_out_dict(self, out: dict[str, Any]) -> str:
        out["message"] = "AUDIT:" + out["message"]
        return self._encoder.encode(out)
```
