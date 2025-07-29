from abc import ABC, abstractmethod

from tools.context import LLMContext


class Base(ABC):

    @abstractmethod
    def handle(self, config: dict, context: LLMContext):
        pass