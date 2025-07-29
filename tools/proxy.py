from tools.base import Base
from tools.context import LLMContext


class Proxy(Base):
    def handle(self, config: dict, ctx: LLMContext):
        if ctx.model in config['tools']['Proxy']['proxy_model'].split(','):
            ctx._proxy = config['tools']['Proxy']['proxy_url']
        return ctx