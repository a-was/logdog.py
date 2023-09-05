import logging

from .base import BaseFormatter
from .logfmt import LogfmtFormatter


class LogMessageWrapper:
    """
    LogMessageWrapper wraps a logging.Logger and provides log message formatting.
    """

    def __init__(
        self,
        logger: logging.Logger,
        *,
        prefix: str = " ",
        suffix: str | None = None,
        formatter: BaseFormatter | None = None,
    ):
        if not isinstance(logger, logging.Logger):
            raise TypeError("logger must be a logging.Logger")
        self.logger = logger

        if not isinstance(prefix, str):
            raise TypeError("prefix must be a string")
        self._prefix = prefix

        if suffix is None:
            suffix = ""
        elif not isinstance(suffix, str):
            raise TypeError("suffix must be a string")
        self._suffix = suffix

        if formatter is None:
            formatter = LogfmtFormatter()
        elif not isinstance(formatter, BaseFormatter):
            raise TypeError(f"formatter must be an instance of {BaseFormatter.__name__}")
        self._formatter = formatter

    def _wrap(self, msg: str, kwargs: dict) -> str:
        if not kwargs:
            return msg
        return msg + self._prefix + self._formatter.format(kwargs) + self._suffix

    def debug(self, msg: str, **kwargs):
        self.logger.debug(
            self._wrap(msg, kwargs),
        )

    def info(self, msg: str, **kwargs):
        self.logger.info(
            self._wrap(msg, kwargs),
        )

    def warning(self, msg: str, **kwargs):
        self.logger.warning(
            self._wrap(msg, kwargs),
        )

    def error(self, msg: str, **kwargs):
        self.logger.error(
            self._wrap(msg, kwargs),
        )

    def exception(self, msg: str, **kwargs):
        self.logger.exception(
            self._wrap(msg, kwargs),
        )

    def critical(self, msg: str, *, exc_info: bool = False, **kwargs):
        self.logger.critical(
            self._wrap(msg, kwargs),
            exc_info=exc_info,
        )
