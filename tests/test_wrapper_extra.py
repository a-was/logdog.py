import json
import logging

from src.logdog import JsonFormatter, LogExtraWrapper
from tests.mock import MockStream

logger = logging.getLogger(__name__)

stream = MockStream()

handler = logging.StreamHandler(stream)
formatter = JsonFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

wrapper = LogExtraWrapper(logger)


def test_extra_wrapper():
    wrapper.info("message", k="v")
    v = stream.getvalue()
    obj = json.loads(v)
    assert obj["k"] == "v"
    assert set(obj.keys()) == {"time", "level", "message", "k"}
