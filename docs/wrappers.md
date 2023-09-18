# Wrappers

## LogMessageWrapper

Message wrapper wraps log message (obviously) and adds context to logs <br />
You can specify `prefix` and `suffix` for this values. Default prefix is single space and no suffix

### Basic usage

```python
import logging

from logdog import LogMessageWrapper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mylogger")

user_id = 1
some_value = "some string"

logger.info("user login", extra={"not": "included", "user": user_id, "value": some_value})
# output: INFO:mylogger:user login

log = LogMessageWrapper(logger)

log.info("user login", user=user_id, action="login", value=some_value)
# output: INFO:mylogger:user login user=1 action=login value="some string"
```

### Custom format

```python
logging.basicConfig(level=logging.INFO, format="%(asctime)s : %(levelname)-8s : %(message)s")
logger = logging.getLogger("mylogger")
log = LogMessageWrapper(logger, prefix=" : ")

log.info("user login", user=user_id, action="login", value=some_value)
# output: 2023-09-05 12:01:09,836 : INFO     : user login : user=1 action=login value="some string"
```

### Different encoder

You can use different encoder for those extra values.
Default is `LogfmtEncoder`, but if you want to encode values as JSON you can use `JsonEncoder` (or your own encoder)

```python
from logdog.encoder import JsonEncoder

log = LogMessageWrapper(
    logger,
    prefix=" [",
    suffix="]",
    encoder=JsonEncoder(),
)

log.info("user login", user=user_id, action="login", value=some_value)
# output: 2023-09-05 12:01:09,836 : INFO     : user login [{"user": 1, "action": "login", "value": "some string"}]
```

### More examples

More examples can be found in `examples/log_message_wrapper.py` file


## LogExtraWrapper

Extra wrapper wraps `kwargs` into `logging.Record`'s `extra` property <br />
It is recommended to use it together with some formatter

### Basic usage

```python
import logging

from logdog import LogMessageWrapper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mylogger")

user_id = 1
some_value = "some string"

# so this
logger.info("user login", extra={"user": user_id, "value": some_value})

log = LogMessageWrapper(logger)
# is the same as this
log.info("user login", user=user_id, value=some_value)
```
