import datetime
import enum
import numbers
from typing import Any

from .base_encoder import BaseEncoder


class LogfmtEncoder(BaseEncoder):
    NONE_STR = "null"
    TRUE_STR = "true"
    FALSE_STR = "false"

    def default(self, obj: Any) -> str:
        raise TypeError(f"object of type '{type(obj).__name__}' is not logfmt serializable")

    def encode(self, obj: dict[str, Any]) -> str:
        return " ".join(f"{k}={self.format_value(v)}" for k, v in obj.items())

    def format_value(self, value: Any) -> str:
        if value is None:
            return self.NONE_STR
        if isinstance(value, str):
            return self._format_string(value)
        if isinstance(value, bool):
            return self.TRUE_STR if value else self.FALSE_STR
        if isinstance(value, numbers.Number):
            return str(value)
        if isinstance(value, dict):
            return self._format_dict(value)
        if isinstance(value, (list, tuple, set)):
            return self._format_list(value)
        if isinstance(value, (datetime.datetime, datetime.date)):
            return value.isoformat()
        if isinstance(value, enum.Enum):
            return value.name
        # if isinstance(value, Exception):
        #     return self._format_string(str(value))
        return self.default(value)

    def _format_list(self, value: list) -> str:
        return "[" + " ".join(self.format_value(v) for v in value) + "]"

    def _format_dict(self, value: dict) -> str:
        return "{" + " ".join(f"{self._format_string(str(k))}={self.format_value(v)}" for k, v in value.items()) + "}"

    def _format_string(self, value: str) -> str:
        match value:
            case "":
                return '""'
            case self.NONE_STR:
                return f'"{self.NONE_STR}"'
            case self.TRUE_STR:
                return f'"{self.TRUE_STR}"'
            case self.FALSE_STR:
                return f'"{self.FALSE_STR}"'
        if '"' in value:
            value = value.replace('"', '\\"')
        if "\n" in value:
            value = value.replace("\n", "\\n")
        if " " in value or "=" in value:
            value = f'"{value}"'
        return value
