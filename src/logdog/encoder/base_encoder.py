from abc import ABC, abstractmethod
from typing import Any


class BaseEncoder(ABC):
    @abstractmethod
    def encode(self, obj: dict[str, Any]) -> str:
        """encode encodes a dict into a string"""
        raise NotImplementedError

    def default(self, obj: Any) -> Any:
        """
        Implement this method in a subclass so it returns a serializable object for `obj`,
        or call the base implementation to raise a `TypeError`

        This works the same as `json.JSONEncoder.default`
        """
        raise TypeError(f"object of type '{type(obj).__name__}' is not serializable")
