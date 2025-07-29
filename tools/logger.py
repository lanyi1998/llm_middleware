import json

from tools.base import Base
from tools.context import LLMContext
from dataclasses import fields


class Logger(Base):
    def handle(self, config: dict, context: LLMContext):
        Logger.looger(config, context)

    @staticmethod
    def looger(config: dict, context: LLMContext):
        print("========================================")
        for field in fields(context):
            field_name = field.name
            if field_name.startswith("__"):
                continue
            field_value = getattr(context, field_name)
            print(f"{field_name}:\t{json.dumps(field_value)}")
        print("========================================")