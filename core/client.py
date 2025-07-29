import json

import httpx
from fastapi.responses import StreamingResponse
from openai import OpenAI
from tools.context import LLMContext


class LLMClient:
    def __init__(self, llm_ctx: LLMContext):
        self.llm_ctx = llm_ctx

    def stream_response(self, llm_response):
        """
        根据配置决定使用伪流式还是真流式响应。
        """
        try:
            # 伪流式处理
            if self.llm_ctx.__pseudo_stream__:
                # 假设 llm_response 是一个包含完整内容的字典，例如：
                # {'choices': [{'message': {'content': '你好！这是一个完整的回答。'}}]}
                # 我们需要从中提取出核心文本

                # 检查响应结构是否有效
                if not hasattr(llm_response, 'choices') or not llm_response.choices:
                    yield "data: [DONE]\n\n"
                    return

                if not hasattr(llm_response.choices[0], 'message') or not hasattr(llm_response.choices[0].message, 'content'):
                    yield "data: [DONE]\n\n"
                    return

                full_content = llm_response.choices[0].message.content

                if not full_content:
                    # 如果没有内容，直接结束
                    yield "data: [DONE]\n\n"
                    return

                # 将完整文本拆分成一个一个的字符，来模拟打字机效果
                # 你也可以按词或句子拆分，但字符效果最平滑
                for char in full_content:
                    # 模拟真实流式中每个 chunk 的结构
                    # 这部分结构需要和你的前端代码相匹配
                    chunk_dict = {
                        "choices": [{
                            "index": 0,
                            "delta": {
                                "content": char
                            }
                        }]
                    }
                    yield f"data: {json.dumps(chunk_dict, ensure_ascii=False)}\n\n"
                    # 加入一个短暂的延迟，让前端能感知到"流"的存在
                    # 延迟时间可以根据需要调整，例如 0.02 秒

                # 所有内容发送完毕后，发送结束标志
                yield "data: [DONE]\n\n"

            # 真流式处理
            else:
                """处理真正的流式响应"""
                # 这里的 llm_response 应该是一个可迭代的生成器
                try:
                    for chunk in llm_response:
                        if hasattr(chunk, 'model_dump'):
                            chunk_dict = chunk.model_dump()
                        else:
                            # 如果没有 model_dump 方法，尝试直接使用 chunk
                            chunk_dict = chunk if isinstance(chunk, dict) else str(chunk)

                        # 确保 chunk_dict 有正确的结构
                        if isinstance(chunk_dict, dict) and 'choices' in chunk_dict:
                            # 确保每个 choice 都有 index 字段
                            for i, choice in enumerate(chunk_dict.get('choices', [])):
                                if 'index' not in choice:
                                    choice['index'] = i

                        yield f"data: {json.dumps(chunk_dict, ensure_ascii=False)}\n\n"
                except Exception as e:
                    # 如果流处理出错，发送错误信息
                    error_dict = {
                        "error": {
                            "message": f"Stream processing error: {str(e)}",
                            "type": "stream_error"
                        }
                    }
                    yield f"data: {json.dumps(error_dict, ensure_ascii=False)}\n\n"

                # 流结束后，发送结束标志
                yield "data: [DONE]\n\n"

        except Exception as e:
            # 顶层异常处理
            error_dict = {
                "error": {
                    "message": f"Response processing error: {str(e)}",
                    "type": "processing_error"
                }
            }
            yield f"data: {json.dumps(error_dict, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"

    def response(self):
        # provider, model_config = self.get_config_by_model(self.llm_ctx.model)
        # if provider == "gemini":
        #     return self.gemini_response()
        # else:
        #     return self.openai_response()
        return self.openai_response()

    def openai_response(self):
        client = self.create_openai_client(self.llm_ctx)
        response = client.chat.completions.create(
            model=self.llm_ctx.model,
            messages=self.llm_ctx.messages,
            stream=self.llm_ctx.stream,
            temperature=self.llm_ctx.temperature,
            extra_body=self.llm_ctx.__extra_body__,
        )
        if self.llm_ctx.stream:
            return StreamingResponse(
                self.stream_response(response),
                media_type="text/plain"
            )
        if self.llm_ctx.__pseudo_stream__:
            return StreamingResponse(
                self.stream_response(response),
                media_type="text/plain"
            )
        else:
            response_dict = response.model_dump()
            return response_dict

    def gemini_response(self):
        client = self.create_gemini_client(self.llm_ctx)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="How does AI work?"
        )
        return response.model_dump()

    # @staticmethod
    # def get_config_by_model(model: str):
    #     for provider, model_config in config.config["model"].items():
    #         if model in model_config['model_name'].split(","):
    #             return provider, model_config

    def create_openai_client(self, cxt: LLMContext):
        # _,mode_config = self.get_config_by_model(cxt.model)
        base_url = cxt.__base_url__
        if base_url.endswith('/chat/completions'):
            base_url = base_url.replace('/chat/completions', '')
        proxy = cxt.__proxy__
        if proxy != '':
            http_client = httpx.Client(
                proxy=proxy,
            )
            client = OpenAI(
                base_url=base_url,
                api_key=cxt.__api_key__,
                http_client=http_client,
            )
        else:
            client = OpenAI(
                base_url=base_url,
                api_key=cxt.__api_key__,
            )
        return client

    # def create_gemini_client(self, cxt: LLMContext):
    #     client = genai.Client()
    #     return client