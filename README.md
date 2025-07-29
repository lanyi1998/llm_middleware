# llm_middleware
LLM中间件，在不修改LLM客户端的情况下，增强LLM客户端

# 使用

`uv sync`

`uvicorn main:app`

原先的base_url: 

`https://dashscope.aliyuncs.com/compatible-mode/v1` 

修改为

`http://127.0.0.1:8000/https://dashscope.aliyuncs.com/compatible-mode/v1`

# 插件

| 插件名    | 功能                      |
| --------- | ------------------------- |
| Logger | 打印请求                  |
| Proxy     | 为指定模型设置代理        |
| QwenMt    | 转换消息为qwen_mt模型格式 |