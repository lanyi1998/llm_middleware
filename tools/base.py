from abc import ABC, abstractmethod

from mcp.context import LLMContext


class Base(ABC):

    @abstractmethod
    def handle(self, config: dict, context: LLMContext):
        pass