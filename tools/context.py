from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class LLMContext:
    model: str
    temperature: float
    messages: list
    stream: bool = False
    __proxy__: str = ''
    __api_key__: str = ''
    __base_url__: str = ''
    __extra_body__: Dict[str, Any] = field(default_factory=dict)
    __pseudo_stream__: bool = False