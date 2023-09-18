# Encoders

Encoders encode `dict[str, Any]` into a `str`

## JsonEncoder

This is very similar encoder to the one from standard library - `json.encoder.JSONEncoder`.
This one has support for the `datetime.datetime`, `datetime.date` and `enum.Enum` types <br />
For `datetime` and `date` it uses the `isoformat()` method. For enum the `name` property is used


## LogfmtEncoder

This encoder encodes into a `key=value` format

Encoding rules can be found in `examples/encoder.py` and `tests/test_encoder_logfmt.py` files.
It also has support for `datetime`, `date` and `Enum` types

### Basic example

```python
from logdog.encoder import LogfmtEncoder

encoder = LogfmtEncoder()

obj = {
    "string": "string",
    "spaces": "with spaces",
    "number": 1.123,
    "list": ["a", "b", "c"],
    "dict": {
        "t": True,
        "f": False,
        "n": None,
    },
    "true": "true",
}

encoder.encode(obj)
# string=string spaces="with spaces" number=1.123 list=[a b c] dict={t=true f=false n=null} true="true"
```


## Custom types support

To add support for encoding custom types, for example `MyType` class,
you can extend existing encoders by overriding their `default` method

```python
from typing import Any

from logdog.encoder import LogfmtEncoder

class MyLogfmtEncoder(LogfmtEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, MyType):
            return f"{obj.some_prop}:{obj.other_prop}"
        return super().default(obj)
```


## Writing your own encoder

You can also create your own encoder

```python
from typing import Any

from logdog.encoder import BaseEncoder

class MyEncoder(BaseEncoder):
    def encode(self, obj: dict[str, Any]) -> str:
        return str(obj)
```
