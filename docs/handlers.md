# Handlers

Logging handlers. You can use them to receive logs in custom destinations

## GoogleChatHandler

This handler allows you to receive logs via Google Chat <br />
[This section](#file-config) describes how to configure handler using `dictConfig`

!!! note

    You may need Google Workspace account to use webhooks

### Usage

```python
import logging

from logdog import GoogleChatHandler

handler = GoogleChatHandler(webhook_url="WEBHOOK_URL")
handler.setLevel(logging.ERROR)
handler.setFormatter(some_formatter)
```

Message is send in format that `some_formatter` keeps

### Params

| Name        | Type  | Default | Description |
|-------------|-------|---------|-------------|
| webhook_url | `str` | `None`  |             |


## BaseBufferedHandler

Buffered handlers collect more logs and **sends them in intervals or when *capacity* is reached**

BaseBufferedHandler has ***starting*** feature

!!! example

    Let's say you set flush interval to 4 hours <br />
    But when application is starting, you don't want to wait
    4 hours to know there were a problem during start <br />
    So this is how starting feature works -
    you set `starting_times` and `starting_intervals`, let's say to 10 and 60.
    It means that in the first 10 times every 60 seconds (so total of 10 minutes)
    handler will send messages in buffer. After 10 times, it will work in standard mode and flush every 4 hours

### Params

| Name              | Type                        | Default  | Description                                         |
|-------------------|-----------------------------|----------|-----------------------------------------------------|
| capacity          | `int` or `None`             | `None`   | Maximum number of logs to keep in buffer. After this value is reached, handler will send messages. If `None` only timed interval will be used |
| flush_interval    | `timedelta`, `int` or `str` | 4 hours  | How long to wait between sending messages in buffer |
| starting_times    | `int` or `None`             | 10       | How many times to wait for `starting_interval` on start. Can be disabled with 0 |
| starting_interval | `timedelta`, `int` or `str` | 1 minute | How long to wait in starting mode                   |

!!! note

    You can use more than one type for the `flush_interval` and `starting_interval` parameters: <br/ >
    - `timedelta`: value is set to the timedelta's duration <br/ >
    - `int`: value is treated as a number of seconds. So, to get 1 hour, set it to 3600. <br/ >
    - `str`: value should be in `[0-9]+[smh]` format, for example `6h`, `45m` or `6h30m10s`

### Message format

???+ example "1 log"

    Collected 1 log created at 2023-10-17 15:51:51.295

    1 - scheduler.py:62::main()

    2023-10-17 15:51:51,295 : ERROR : __main__ : zero raised <br />
    Traceback (most recent call last): <br />
    File ".../scheduler.py", line 62, in main <br />
    1 / 0 <br />
    ZeroDivisionError: division by zero

    -- End of message --


??? example "Multiple logs"

    Collected 20 logs created between 2023-10-17 15:42:51.295 and 2023-10-17 15:43:14.301

    8 - scheduler.py:62::main() <br />
    12 - scheduler.py:87::process_message()

    2023-10-17 15:42:51.295 : ERROR : __main__ : zero raised <br />
    Traceback (most recent call last): <br />
    File ".../scheduler.py", line 62, in main <br />
    1 / 0 <br />
    ZeroDivisionError: division by zero

    2023-10-17 2023-10-17 15:42:51.482 : ERROR : __main__ : another zero raised <br />
    Traceback (most recent call last): <br />
    File ".../scheduler.py", line 62, in main <br />
    1 / 0 <br />
    ZeroDivisionError: division by zero

    2023-10-17 2023-10-17 15:42:52.052 : ERROR : __main__ : another zero raised <br />
    Traceback (most recent call last): <br />
    File ".../scheduler.py", line 62, in main <br />
    1 / 0 <br />
    ZeroDivisionError: division by zero

    *more messages...*

    -- End of message --


## BufferedSmtpHandler

Works like standard lib's SMTP handler, but it's buffered.
It also means it has *starting* feature. <br />
[This section](#file-config) describes how to configure handler using `dictConfig`

### Params

| Name                           | Type                 | Default | Description                                       |
|--------------------------------|----------------------|---------|---------------------------------------------------|
| host                           | `str`                |         |                                                   |
| port                           | `int`                |         |                                                   |
| user                           | `str` or `None`      | `None`  |                                                   |
| password                       | `str` or `None`      | `None`  |                                                   |
| sender                         | `str`                |         |                                                   |
| receivers                      | `list[str]` or `str` |         | String in `me@example.com;you@example.com` format |
| subject                        | `str`                |         |                                                   |
| use_starttls                   | `bool`               | `True`  |                                                   |
| use_ssl                        | `bool`               | `False` |                                                   |
| + `BaseBufferedHandler` params                                                                                      |


## BufferedGoogleChatHandler

Works like GoogleChatHandler, but it's buffered. It also means it has *starting* feature. <br />
[This section](#file-config) describes how to configure handler using `dictConfig`

### Params

| Name        | Type  | Default | Description |
|-------------|-------|---------|-------------|
| webhook_url | `str` | `None`  |             |
| + `BaseBufferedHandler` params              |

## File config

Using dict config

```python
{
    "handlers": {
        "smtp": {
            "()": "logdog.BufferedSmtpHandler",  # or logdog.BufferedGoogleChatHandler
            "host": "localhost",
            "port": 25,
            ...
        },
    },
}
```

!!! tip
    Check `examples/logging_config.py` for full example


## Writing your own buffered handler

You can create your own buffered formatter

```python
from logdog.handler import BaseBufferedHandler

class MyHandler(BaseBufferedHandler):
    def flush(self):
        if len(self.buffer) == 0:
            return
        message = self.build_message()
        with self.lock:
            try:
                // send message somewhere
            except Exception:
                self.handleError(self.buffer[-1])
            finally:
                // close connection here and clear buffer
                self.buffer.clear()
```
