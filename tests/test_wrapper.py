import logging

import pytest

from src.logdog.wrapper import JsonRenderer, LogMessageWrapper

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
            LogMessageWrapper(logger, renderer=JsonRenderer()),
            'message {"k": "v"}',
        ),
        (
            LogMessageWrapper(logger, prefix=" [", suffix="]", renderer=JsonRenderer()),
            'message [{"k": "v"}]',
        ),
        (
            LogMessageWrapper(logger, prefix=" : ", renderer=JsonRenderer()),
            'message : {"k": "v"}',
        ),
    ],
)
def test_prefix_and_suffix(wrapper, expected):
    assert wrapper._wrap("message", {"k": "v"}) == expected
