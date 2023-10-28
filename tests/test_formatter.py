import logging
import logging.handlers
import sys

import pytest

from src.logdog import JsonFormatter, LogfmtFormatter
from src.logdog.exceptions import UnsupportedPythonVersionError
from tests.mock import MockStream

logger = logging.getLogger(__name__)

stream = MockStream()

handler = logging.StreamHandler(stream)
handler.setLevel(logging.DEBUG)
formatter = JsonFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


@pytest.mark.parametrize(
    "formats,expected",
    [
        (
            # create default keys dict
            [
                None,
                "",
                "time",
                "time level",
                "message",
                "message:message",
                "time level message exception",
                "time:time level:level message:message exception:exception",
            ],
            {
                "time": "time",
                "level": "level",
                "message": "message",
                "exception": "exception",
            },
        ),
        (
            # disable all defaults
            "time:- level:- message:- exception:-",
            {},
        ),
        (
            # disable some defaults
            [
                "time level:- exception:-",
                "level:- exception:-",
            ],
            {
                "time": "time",
                "message": "message",
            },
        ),
        (
            # create aliases
            "time:ts level:- message:msg exception:exc",
            {
                "time": "ts",
                "message": "msg",
                "exception": "exc",
            },
        ),
        (
            # enable all keys
            "levelno logger filename funcName lineno module pathname process processName thread threadName",
            {
                "time": "time",
                "level": "level",
                "levelno": "levelno",
                "message": "message",
                "logger": "logger",
                "filename": "filename",
                "funcName": "funcName",
                "lineno": "lineno",
                "module": "module",
                "pathname": "pathname",
                "process": "process",
                "processName": "processName",
                "thread": "thread",
                "threadName": "threadName",
                "exception": "exception",
            },
        ),
        (
            # enable all keys with aliases
            "logger:name filename:file funcName:fn lineno:line module:module pathname:path processName:process threadName:thread",
            {
                "time": "time",
                "level": "level",
                "message": "message",
                "logger": "name",
                "filename": "file",
                "funcName": "fn",
                "lineno": "line",
                "module": "module",
                "pathname": "path",
                "processName": "process",
                "threadName": "thread",
                "exception": "exception",
            },
        ),
        (
            # disable all default keys and add some others
            "time:- level:- message:- exception:- filename:file funcName:fn lineno",
            {
                "filename": "file",
                "funcName": "fn",
                "lineno": "lineno",
            },
        ),
        (
            # disable all default keys and add some others
            "level:- levelno:level",
            {
                "time": "time",
                "message": "message",
                "exception": "exception",
                "levelno": "level",
            },
        ),
        (
            # "-" as value are not alias
            "time:- level:- message:- exception:- module:- filename:-",
            {},
        ),
    ],
)
def test_keys_formats(formats, expected):
    if isinstance(formats, str):
        formats = [formats]
    for format in formats:
        formatter = LogfmtFormatter(format)
        assert expected == formatter._keys
        formatter = JsonFormatter(format)
        assert expected == formatter._keys


@pytest.mark.parametrize(
    "format",
    [
        "unknown:-",
        "time message:time",
        "lineno lineno",
        "time:- time",
        "time time:-",
        "levelno:level",
        "filename:module module",
        "filename:module module:module",
        "filename:alias module:alias",
    ],
)
def test_invalid_format(format):
    with pytest.raises(ValueError):
        JsonFormatter(format)
    with pytest.raises(ValueError):
        LogfmtFormatter(format)


@pytest.mark.skipif(sys.version_info >= (3, 12), reason="Python < 3.12 required")
def test_keys_format_below_version_3_12():
    with pytest.raises(UnsupportedPythonVersionError):
        JsonFormatter("taskName")
    with pytest.raises(UnsupportedPythonVersionError):
        LogfmtFormatter("taskName")


@pytest.mark.skipif(sys.version_info < (3, 12), reason="Python 3.12+ required")
def test_keys_format_above_version_3_12():
    formatter = LogfmtFormatter("taskName")
    assert "taskName" in formatter._keys
    formatter = JsonFormatter("taskName")
    assert "taskName" in formatter._keys
