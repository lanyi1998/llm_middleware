from tools.base import Base
from tools.context import LLMContext


class QwenMt(Base):
    def handle(self, config: dict, ctx: LLMContext):
        if ctx.model in ["qwen-mt-turbo", "qwen-mt-plus"]:
            ctx.__pseudo_stream__ = True
            ctx.stream = False
            translation_options = {
                "source_lang": "auto",
                "target_lang": "English"
            }
            ctx.messages = [
                {
                    "role": "user",
                    "content": ctx.messages[len(ctx.messages)-1]["content"]
                }
            ]
            ctx.__extra_body__ = {
                "translation_options": translation_options
            }
            # ctx.messages = messages
        return ctx