import datetime
import enum
import numbers
from typing import Any

from .base import BaseFormatter


class LogfmtFormatter(BaseFormatter):
    NONE_STR = "null"
    TRUE_STR = "true"
    FALSE_STR = "false"

    def format(self, obj: dict) -> str:
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
        return self._format_string(str(value))

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
