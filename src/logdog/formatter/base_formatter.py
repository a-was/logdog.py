import contextlib
import logging
import re
import sys
import traceback
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from ..exceptions import UnsupportedPythonVersionError
from .common import (
    TimeFormat,
    re_fmt,
    standard_logging_record_attrs,
    supported_keys,
    supported_since_python_version,
)


class BaseFormatter(ABC, logging.Formatter):
    def __init__(
        self,
        keys: str | None = None,
        *args: Any,
        time_fmt: TimeFormat | str = TimeFormat.DEFAULT,
        include_ms: bool = True,
    ):
        if keys is None:
            keys = ""
        elif not isinstance(keys, str):
            raise TypeError("keys must be a string")

        if not isinstance(time_fmt, (TimeFormat, str)):
            raise TypeError("time_fmt must be a TimeFormat or a string")

        if not isinstance(include_ms, bool):
            raise TypeError("include_ms must be a boolean")

        with contextlib.suppress(ValueError, TypeError):
            time_fmt = TimeFormat(time_fmt)

        self._parse_keys(keys)

        for key, version in supported_since_python_version.items():
            if key in self._keys and version > sys.version_info:
                min_version = f"{version[0]}.{version[1]}"
                current_version = f"{sys.version_info[0]}.{sys.version_info[1]}"
                raise UnsupportedPythonVersionError(
                    f"Key '{key}' requires Python {min_version}, but {current_version} is used"
                )

        self._use_datetime = False
        self._timestamp_format_fn = None

        match time_fmt:
            case TimeFormat.DEFAULT:
                self.default_time_format = "%Y-%m-%d %H:%M:%S"
                self.default_msec_format = "%s,%03d" if include_ms else None
            case TimeFormat.ISO:
                self.default_time_format = "%Y-%m-%dT%H:%M:%S"
                self.default_msec_format = "%s.%03d" if include_ms else None
            case TimeFormat.ISO_TIMEZONE:
                self._use_datetime = True
            case TimeFormat.TIMESTAMP:
                self._timestamp_format_fn = int
            case TimeFormat.TIMESTAMP_FLOAT:
                self._timestamp_format_fn = lambda x: x
            case TimeFormat.TIMESTAMP_MILLISECONDS:
                self._timestamp_format_fn = lambda x: int(x * 1000)
            case TimeFormat.TIMESTAMP_MICROSECONDS:
                self._timestamp_format_fn = lambda x: int(x * 1_000_000)
            case TimeFormat.TIMESTAMP_NANOSECONDS:
                self._timestamp_format_fn = lambda x: int(x * 1_000_000_000)
            case str():
                self.default_time_format = time_fmt
                self.default_msec_format = "%s.%03d" if include_ms else None
            case _:
                raise NotImplementedError(f"Unknown time format: {time_fmt}")

    @staticmethod
    def _sort_matches(matches: list[re.Match[str]]):
        """sort matches so elements with alias value "-" are first, then None and then the rest"""
        weights = {
            "-": 1,
            None: 2,
        }
        default = max(weights.values()) + 1

        matches.sort(key=lambda x: weights.get(x.group(2), default))

    def _parse_keys(self, keys: str):
        default_keys = {
            "time": "time",
            "level": "level",
            "message": "message",
            "exception": "exception",
        }
        user_keys = {}

        matches = list(re_fmt.finditer(keys))
        self._sort_matches(matches)

        checked_keys = []

        for m in matches:
            key = m.group(1)
            if key not in supported_keys:
                raise ValueError(f"Unknown key: {key}")
            if key in checked_keys:
                raise ValueError(f"Duplicate key: {key}")
            checked_keys.append(key)

            alias = m.group(2)
            if not alias or alias == key:
                if key in user_keys.values():
                    raise ValueError(f"Duplicate key: {key}")
                user_keys[key] = key
                continue
            if alias == "-":
                if key in default_keys:
                    del default_keys[key]
                continue
            if alias in default_keys:
                raise ValueError(f"Duplicate key: {alias}")
            if alias in user_keys.values():
                raise ValueError(f"Duplicate key: {alias}")
            user_keys[key] = alias

        self._keys = default_keys | user_keys

    def format(self, record: logging.LogRecord) -> str:
        out = {}
        for source_key, target_key in self._keys.items():
            match source_key:
                case "time":
                    if self._timestamp_format_fn:
                        out[target_key] = self._timestamp_format_fn(record.created)
                    elif self._use_datetime:
                        out[target_key] = (
                            datetime.fromtimestamp(record.created).astimezone().isoformat(timespec="milliseconds")
                        )
                    else:
                        out[target_key] = super().formatTime(record)
                case "level":
                    out[target_key] = record.levelname
                case "levelno":
                    out[target_key] = record.levelno
                case "message":
                    out[target_key] = record.getMessage()
                case "exception":
                    if record.exc_info:
                        out[target_key] = self._format_exception(record.exc_info)
                case "logger":
                    out[target_key] = record.name
                case _:
                    out[target_key] = getattr(record, source_key)

        # extra keys
        for key in set(record.__dict__.keys()) - standard_logging_record_attrs:
            out[key] = record.__dict__[key]

        return self._format_out_dict(out)

    def _format_exception(self, exc_info) -> str:
        exc = []
        for line in traceback.format_exception(*exc_info):
            for subline in line.split("\n"):
                s = subline.strip()
                if s == "":
                    continue
                exc.append(s)
        return exc

    @abstractmethod
    def _format_out_dict(self, out: dict[str, Any]) -> str:
        raise NotImplementedError
