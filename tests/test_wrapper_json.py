from datetime import date, datetime, timedelta, timezone
from enum import Enum

import pytest

from src.logdog.wrapper import JsonRenderer

renderer = JsonRenderer()


@pytest.mark.parametrize(
    "kwargs,expected",
    [
        ({"a": 1}, '{"a": 1}'),
    ],
)
def test_render_kwargs(kwargs, expected):
    assert renderer.render(kwargs) == expected


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
    assert renderer.render({"value": value}) == f'{{"value": "{expected}"}}'


def test_format_enum():
    # For enum type `name` property will be used.
    class LanguageEnum(Enum):
        ENGLISH = "en"

    language = LanguageEnum.ENGLISH
    assert renderer.render({"value": language}) == f'{{"value": "{language.name}"}}'
