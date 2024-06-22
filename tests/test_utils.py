import pytest

from src.logdog import _util


@pytest.mark.parametrize(
    "format,seconds",
    [
        ("", 0),
        ("invalid", 0),
        ("7x", 0),
        ("30s", 30),
        ("10m", 60 * 10),
        ("2h", 60 * 60 * 2),
        ("2h30m15s", 60 * 60 * 2 + 60 * 30 + 15),
        ("0h0m1s", 1),
    ],
)
def test_parse_duration(format, seconds):
    assert _util.duration.parse_duration(format) == seconds
