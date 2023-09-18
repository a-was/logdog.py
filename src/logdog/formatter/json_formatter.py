from typing import Any

from ..encoder import JsonEncoder
from .base_formatter import BaseFormatter


class JsonFormatter(BaseFormatter):
    _encoder = JsonEncoder()

    def _format_out_dict(self, out: dict[str, Any]) -> str:
        return self._encoder.encode(out)
