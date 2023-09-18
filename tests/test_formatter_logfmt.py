import logging

from src.logdog import LogExtraWrapper, LogfmtFormatter
from tests.mock import MockStream

logger = logging.getLogger(__name__)

stream = MockStream()

handler = logging.StreamHandler(stream)
formatter = LogfmtFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

wrapper = LogExtraWrapper(logger)


def test_logfmt_formatter():
    wrapper.info(
        "message",
        k="v",
        user_id=2,
    )
    v = stream.getvalue()

    assert "level=INFO" in v
    assert "message=message" in v
    assert "k=v" in v
    assert "user_id=2" in v
