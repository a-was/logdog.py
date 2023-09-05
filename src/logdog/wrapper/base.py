from abc import ABC, abstractmethod


class BaseRenderer(ABC):
    @abstractmethod
    def render(self, obj: dict) -> str:
        raise NotImplementedError
