import datetime
import enum
import json
from typing import Any

from .base_encoder import BaseEncoder


class JsonEncoder(BaseEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        if isinstance(obj, enum.Enum):
            return obj.name
        return json.JSONEncoder().default(obj)

    def encode(self, obj: dict[str, Any]) -> str:
        return json.dumps(obj, default=self.default)
