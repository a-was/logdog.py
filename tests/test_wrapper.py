import logging

import pytest
from logdog import LogMessageWrapper

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "wrapper,expected",
    [
        (
            LogMessageWrapper(logger),
            "message k=v",
        ),
        (
            LogMessageWrapper(logger, prefix=" [", suffix="]"),
            "message [k=v]",
        ),
        (
            LogMessageWrapper(logger, prefix=" : "),
            "message : k=v",
        ),
    ],
)
def test_prefix_and_suffix(wrapper, expected):
    assert wrapper._wrap("message", {"k": "v"}) == expected
