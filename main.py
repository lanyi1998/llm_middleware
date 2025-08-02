import importlib
import pkgutil

from fastapi import FastAPI, Request

import tools
from config import config
from core.client import LLMClient

app = FastAPI()
ToolRegistry = {}


def main():
    global ToolRegistry
    config.config = config.load_config("config.yaml")
    for _, name, _ in pkgutil.walk_packages(tools.__path__, tools.__name__ + '.'): 
        importlib.import_module(name)
        
    ToolRegistry = {cls.__name__: cls for cls in tools.base.Base.__subclasses__()} #注册工具


main()


def request_conversion(request: Request, body: dict):
    cxt = tools.context.LLMContext(**body) 
    authorization: str = request.headers.get("Authorization") 
    token = ''
    if authorization:
        token = authorization.split(" ")[1]
    cxt.__api_key__ = token
    base_url = request.url.path[1:]
    cxt.__base_url__ = base_url
    return cxt


@app.middleware("http")
async def llm_middleware(request: Request, call_next):
    # TODO: 兼容gemini接口
    body_dict = await request.json()
    cxt = request_conversion(request, body_dict)
    # direct_subclasses = tools.base.Base.__subclasses__() 
    # for cls in direct_subclasses:
    #     if cls.__name__ not in config.config['tools']['Enable']:
    #          continue
    #     c = cls().handle(config.config, cxt)
    #     if c:
    #         cxt = c
    for tool_name in config.config['tools']['Enable']:
        cls = ToolRegistry.get(tool_name)
        if cls:
            new_cxt = cls().handle(config.config,cxt)
            if new_cxt:
                cxt = new_cxt
    request.state.llm_cxt = cxt
    response = await call_next(request)
    return response


@app.post("/{full_url:path}")
def index(request: Request):
    """
    OpenAI 兼容的聊天接口
    """
    llm = LLMClient(request.state.llm_cxt)
    return llm.response()
