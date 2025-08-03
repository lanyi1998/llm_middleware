from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class LLMContext:
    model: str
    temperature: float
    messages: list
    stream: bool = False
    top_p: float = 1.0
    stream_options: Dict[str, Any] = field(default_factory=dict) #默认创建一个为空的
    __proxy__: str = ''
    __api_key__: str = ''
    __base_url__: str = ''
    __extra_body__: Dict[str, Any] = field(default_factory=dict)
    __pseudo_stream__: bool = False