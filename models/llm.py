from openai import OpenAI
from config.settings import settings
from core.message import Message
from tools.base import BaseTool

class ChatLLM:

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL
        )

    def invoke(self, messages:list[dict],tools:BaseTool=None):
        response = self.client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=messages,
            temperature=settings.TEMPERATURE,
            tools=tools
        )

        return response.choices[0].message # 因为有些接口允许llm返回多个答案，也就是choices是一个列表，正常来说只有一个回复，但也需要取[0]
