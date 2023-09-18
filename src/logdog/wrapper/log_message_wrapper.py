import logging
from typing import Any

from ..encoder import BaseEncoder, LogfmtEncoder


class LogMessageWrapper:
    """
    LogMessageWrapper wraps a logging.Logger and provides log message formatting
    """

    def __init__(
        self,
        logger: logging.Logger,
        *,
        prefix: str = " ",
        suffix: str | None = None,
        encoder: BaseEncoder | None = None,
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

        if encoder is None:
            encoder = LogfmtEncoder()
        elif not isinstance(encoder, BaseEncoder):
            raise TypeError(f"encoder must be an instance of {BaseEncoder.__name__}")
        self._encoder = encoder

    def _wrap(self, msg: str, kwargs: dict[str, Any]) -> str:
        if not kwargs:
            return msg
        return msg + self._prefix + self._encoder.encode(kwargs) + self._suffix

    def debug(self, msg: str, **kwargs):
        self.logger.debug(
            self._wrap(msg, kwargs),
            stacklevel=2,
        )

    def info(self, msg: str, **kwargs):
        self.logger.info(
            self._wrap(msg, kwargs),
            stacklevel=2,
        )

    def warning(self, msg: str, **kwargs):
        self.logger.warning(
            self._wrap(msg, kwargs),
            stacklevel=2,
        )

    def error(self, msg: str, **kwargs):
        self.logger.error(
            self._wrap(msg, kwargs),
            stacklevel=2,
        )

    def exception(self, msg: str, **kwargs):
        self.logger.exception(
            self._wrap(msg, kwargs),
            stacklevel=3,
        )

    def critical(self, msg: str, *, exc_info: bool = False, **kwargs):
        self.logger.critical(
            self._wrap(msg, kwargs),
            exc_info=exc_info,
            stacklevel=2,
        )
