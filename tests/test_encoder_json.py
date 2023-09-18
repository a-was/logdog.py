from datetime import date, datetime, timedelta, timezone
from enum import Enum

import pytest

from src.logdog import JsonEncoder

encoder = JsonEncoder()


@pytest.mark.parametrize(
    "value",
    [
        # Unknown types will raise an exception
        Exception("exception"),
    ],
)
def test_invalid_types(value):
    with pytest.raises(TypeError):
        encoder.encode(value)


@pytest.mark.parametrize(
    "value,expected",
    [
        # For date / datetime type `isoformat()` method will be used
        (date(2023, 9, 5), "2023-09-05"),
        (datetime(2023, 9, 5, 12, 24, 40, 123456), "2023-09-05T12:24:40.123456"),
        (
            datetime(2023, 9, 5, 12, 24, 40, 123456, tzinfo=timezone(timedelta(hours=2))),
            "2023-09-05T12:24:40.123456+02:00",
        ),
    ],
)
def test_format_datetime(value, expected):
    assert encoder.encode({"value": value}) == f'{{"value": "{expected}"}}'


def test_format_enum():
    # For enum type `name` property will be used.
    class LanguageEnum(Enum):
        ENGLISH = "en"

    language = LanguageEnum.ENGLISH
    assert encoder.encode({"value": language}) == f'{{"value": "{language.name}"}}'


@pytest.mark.parametrize(
    "obj,expected",
    [
        ({"a": 1, "b": "value"}, '{"a": 1, "b": "value"}'),
        ({"k1": "v1", "k2": ["v2", "v3"]}, '{"k1": "v1", "k2": ["v2", "v3"]}'),
        ({"dict": {"dict key": "dict value"}}, '{"dict": {"dict key": "dict value"}}'),
    ],
)
def test_encode(obj, expected):
    assert encoder.encode(obj) == expected
