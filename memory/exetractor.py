import json
from models.llm import ChatLLM


class MemoryExtractor:

    def __init__(self):
        self.llm = ChatLLM()

    def extract(self, messages):

        conversation = []

        for msg in messages:
            conversation.append(
                f"{msg.role}: {msg.content}"
            )

        text = "\n".join(conversation)

        prompt = f"""
你是一个长期记忆提取器。

请分析下面的对话，只提取未来对话仍然可能有价值的信息。

适合保存：
- 用户长期偏好
- 用户长期目标
- 已经明确确定的重要项目约束
- 后续任务需要持续使用的信息

不要保存：
- 普通寒暄
- 临时问题
- 一次性的短期信息
- 无长期价值的回答内容

如果没有值得保存的信息，返回：

{{"memories": []}}

如果有，返回：

{{
  "memories": [
    "记忆1",
    "记忆2"
  ]
}}

只返回JSON。

对话：

{text}
"""

        response = self.llm.invoke(
            [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response.content

        data = json.loads(content)

        return data["memories"]