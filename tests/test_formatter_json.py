import json
import logging
import logging.handlers

from src.logdog import JsonFormatter, LogExtraWrapper
from tests.mock import MockStream

logger = logging.getLogger(__name__)

stream = MockStream()

handler = logging.StreamHandler(stream)
handler.setLevel(logging.DEBUG)
formatter = JsonFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

wrapper = LogExtraWrapper(logger)


def test_json_formatter():
    wrapper.info(
        "message",
        k="v",
        user_id=2,
    )
    d = json.loads(stream.getvalue())
    assert d["k"] == "v"
    assert d["user_id"] == 2
    expected = {
        "time",
        "level",
        "message",
        "k",
        "user_id",
    }
    assert set(d.keys()) == expected
