import datetime
import enum
import json
from typing import Any

from .base import BaseRenderer


class JsonEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        if isinstance(obj, enum.Enum):
            return obj.name
        return super().default(obj)


class JsonRenderer(BaseRenderer):
    def render(self, obj: dict) -> str:
        return json.dumps(obj, cls=JsonEncoder)
