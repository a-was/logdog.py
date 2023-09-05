from datetime import date, datetime, timedelta, timezone
from enum import Enum

import pytest
from logdog.wrapper import LogfmtFormatter

formatter = LogfmtFormatter()


@pytest.mark.parametrize(
    "value,expected",
    [
        # If the string contains a space, then it must be quoted.
        (" ", '" "'),
        # If the string contains a equals sign, then it must be quoted.
        ("=", '"="'),
        # All double quotes must be escaped.
        ('"', '\\"'),
        # If the string requires escaping and quoting, then both
        # operations should be performed.
        (' "', '" \\""'),
        # If the string is empty, then it should be quoted.
        ("", '""'),
        # If the string contains a newline, then it should be escaped.
        ("\n", "\\n"),
        ("\n\n", "\\n\\n"),
    ],
)
def test_format_string(value, expected):
    assert formatter._format_string(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        # Numbers will be converted to their string representation using `str`.
        (1, "1"),
        (2.04, "2.04"),
        # Strings will be passed through the `format_string` function.
        ("=", '"="'),
        # Objects will be converted to their string representation using `str`.
        (Exception("="), '"="'),
        # None, True and False will be converted to their string representation.
        # Their string representations will be quoted.
        (None, "null"),
        ("null", '"null"'),
        (True, "true"),
        ("true", '"true"'),
        (False, "false"),
        ("false", '"false"'),
    ],
)
def test_format_value(value, expected):
    assert formatter.format_value(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        # Lists items will be separated by spaces and quoted if necessary.
        ([1, 2, 3], "[1 2 3]"),
        ({1, 2, 3}, "[1 2 3]"),
        (["a", "b b"], '[a "b b"]'),
        (({"a": "b"}, {"c": "d d", "e": "f"}), '[{a=b} {c="d d" e=f}]'),
    ],
)
def test_format_list(value, expected):
    assert formatter.format_value(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        # Dictionaries items will be separated by spaces and quoted (keys and values) if necessary.
        ({"a": 1}, "{a=1}"),
        ({"a": 1, "b": 2}, "{a=1 b=2}"),
        ({"a": " "}, '{a=" "}'),
        ({"k1": "v1", "k2": ["v2", "v3"]}, "{k1=v1 k2=[v2 v3]}"),
        ({"nested": {"nested key": "nested value"}}, '{nested={"nested key"="nested value"}}'),
    ],
)
def test_format_dict(value, expected):
    assert formatter.format_value(value) == expected


@pytest.mark.parametrize(
    "kwargs,expected",
    [
        ({"a": 1}, "a=1"),
        ({"a": 1, "b": 2}, "a=1 b=2"),
        ({"a": " "}, 'a=" "'),
        ({"k1": "v1", "k2": ["v2", "v3"]}, "k1=v1 k2=[v2 v3]"),
        ({"dict": {"dict key": "dict value"}}, 'dict={"dict key"="dict value"}'),
    ],
)
def test_format_kwargs(kwargs, expected):
    assert formatter.format(kwargs) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        # For date / datetime type isoformat will be used.
        (date(2023, 9, 5), "2023-09-05"),
        (datetime(2023, 9, 5, 12, 24, 40, 123456), "2023-09-05T12:24:40.123456"),
        (
            datetime(2023, 9, 5, 12, 24, 40, 123456, tzinfo=timezone(timedelta(hours=2))),
            "2023-09-05T12:24:40.123456+02:00",
        ),
    ],
)
def test_format_datetime(value, expected):
    assert formatter.format_value(value) == expected


def test_format_enum():
    # For enum type `name` property will be used.
    class LanguageEnum(Enum):
        ENGLISH = "en"

    language = LanguageEnum.ENGLISH
    assert formatter.format_value(language) == language.name
