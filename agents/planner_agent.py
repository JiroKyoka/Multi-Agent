from agents.base_agent import BaseAgent
from models.llm import ChatLLM
from core.message import Message
from core.task import TaskPlan,Task
import json

class PlannerAgent(BaseAgent):

    def __init__(self, agent_specs=None):
        super().__init__("planner")
        self.llm = ChatLLM()
        self.agent_specs = agent_specs or []

    def run(self, state):
        user_task = state["task"]
        if not user_task and state["messages"]:
            user_task = state["messages"][-1].content

        agent_text = "\n".join(
            f"- {agent['name']}：{agent['description']}"
            for agent in self.agent_specs
        )

        prompt = f"""
                你是任务规划器。

                用户任务：{user_task}

                请把用户任务拆解成任务计划。

                可用 agent：
                {agent_text}

                要求：
                1. agent 字段必须从可用 agent 的 name 中选择。
                2. 根据每个 agent 的 description 判断该子任务应该分配给谁。
                3. 不允许创造新的 agent name。

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

        plan = TaskPlan(
            tasks=[
                Task(
                    name=item["name"],
                    agent=item["agent"],
                    description=item["description"]
                )
                for item in data["tasks"]
            ]
        )
        state["plan"] = plan
        state["result"] = response.content
        state["messages"].append(
            Message(
                role="assistant",
                content=response.content
            )
        )

        return state
