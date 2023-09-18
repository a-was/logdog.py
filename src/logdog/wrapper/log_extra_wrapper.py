import logging


class LogExtraWrapper:
    """
    LogExtraWrapper wraps a logging.Logger and provides it's `extra` param creation based on `kwargs`
    """

    def __init__(self, logger: logging.Logger):
        if not isinstance(logger, logging.Logger):
            raise TypeError("logger must be a logging.Logger")
        self.logger = logger

    def debug(self, msg: str, **kwargs):
        self.logger.debug(
            msg,
            stacklevel=2,
            extra=kwargs,
        )

    def info(self, msg: str, **kwargs):
        self.logger.info(
            msg,
            stacklevel=2,
            extra=kwargs,
        )

    def warning(self, msg: str, **kwargs):
        self.logger.warning(
            msg,
            stacklevel=2,
            extra=kwargs,
        )

    def error(self, msg: str, **kwargs):
        self.logger.error(
            msg,
            stacklevel=2,
            extra=kwargs,
        )

    def exception(self, msg: str, **kwargs):
        self.logger.exception(
            msg,
            stack_info=True,
            stacklevel=3,
            extra=kwargs,
        )

    def critical(self, msg: str, *, exc_info: bool = False, **kwargs):
        self.logger.critical(
            msg,
            exc_info=exc_info,
            stacklevel=2,
            extra=kwargs,
        )
