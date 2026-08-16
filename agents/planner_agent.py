from agents.base_agent import BaseAgent
from models.llm import ChatLLM
from core.message import Message
from core.task import TaskPlan,Task
import json

class PlannerAgent(BaseAgent):

    def __init__(self):
        super().__init__("planner")
        self.llm = ChatLLM()

    def run(self, state):
        prompt = f"""
你是任务规划器。

用户任务：{state["messages"][-1].content}

请把用户任务拆解成任务计划。

只输出 JSON，不要输出解释文字。

JSON 格式必须是：
{{
  "tasks": [
    {{
      "name": "任务名称",
      "agent": "负责该任务的 agent 名称",
      "description": "任务描述"
    }}
  ]
}}
"""

        response = self.llm.invoke([    
            {
                "role": "system",
                "content": prompt
            }
        ])
        data = json.loads(response.content)

        state["plan"] = TaskPlan(
            tasks=[
                Task(
                    name=item["name"],
                    agent=item["agent"],
                    description=item["description"]
                )
                for item in data["tasks"]
            ]
        )

        return state