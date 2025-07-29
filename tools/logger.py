from mcp.base import Base
from mcp.context import LLMContext
from dataclasses import fields


class LLMLogger(Base):
    def handle(self, config: dict, context: LLMContext):
        LLMLogger.looger(config, context)

    @staticmethod
    def looger(config: dict, context: LLMContext):
        print("========================================")
        for field in fields(context):
            field_name = field.name
            field_value = getattr(context, field_name)
            field_type = field.type
            print(f"{field_name}:{field_value}")
        print("========================================")