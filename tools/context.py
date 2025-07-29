from dataclasses import dataclass

@dataclass
class LLMContext:
    model: str
    temperature: float
    messages: list
    stream: bool = False