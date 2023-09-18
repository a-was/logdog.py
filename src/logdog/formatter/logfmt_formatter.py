from typing import Any

from ..encoder import LogfmtEncoder
from .base_formatter import BaseFormatter


class LogfmtFormatter(BaseFormatter):
    _encoder = LogfmtEncoder()

    def _format_out_dict(self, out: dict[str, Any]) -> str:
        return self._encoder.encode(out)
