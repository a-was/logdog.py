# logdog

Python package with `logging` utilities

# Requirements

- Python >= 3.10

# Installation

```bash
pip install -U python-logdog
```

# Usage

> [!NOTE]
> These are only basic examples.
> More advanced ones can be found in the `examples/` directory

## Message wrapper

### Basic

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

### Renderers

Currently there are 2 renderers:

- `LogfmtRenderer` (default one)
- `JsonRenderer`

Same simple example using different renderer:

```python
from logdog.wrapper import JsonRenderer, LogMessageWrapper

logging.basicConfig(level=logging.INFO, format="%(asctime)s : %(levelname)-8s : %(message)s")
logger = logging.getLogger("mylogger")
log = LogMessageWrapper(
    logger,
    prefix=" [",
    suffix="]",
    renderer=JsonRenderer(),
)

log.info("user login", user=user_id, action="login", value=some_value)
# output: 2023-09-05 12:01:09,836 : INFO     : user login [{"user": 1, "action": "login", "value": "some string"}]
```
