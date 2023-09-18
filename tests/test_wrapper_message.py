import logging

import pytest

from src.logdog import JsonEncoder, LogMessageWrapper

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
        (
            LogMessageWrapper(logger, encoder=JsonEncoder()),
            'message {"k": "v"}',
        ),
        (
            LogMessageWrapper(logger, prefix=" [", suffix="]", encoder=JsonEncoder()),
            'message [{"k": "v"}]',
        ),
        (
            LogMessageWrapper(logger, prefix=" : ", encoder=JsonEncoder()),
            'message : {"k": "v"}',
        ),
    ],
)
def test_message_wrapper(wrapper, expected):
    assert wrapper._wrap("message", {"k": "v"}) == expected

