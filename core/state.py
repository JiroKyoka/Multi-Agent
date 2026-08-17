from typing import TypedDict, List
from core.message import Message
from core.task import TaskPlan

class AgentState(TypedDict):
    task : str
    messages : List[Message]
    result : str
    plan : TaskPlan | None
    current_task : dict | None
    task_results : List[dict]

def ensure_state_defaults(state: AgentState) -> AgentState:
    state.setdefault("task", "")
    state.setdefault("messages", [])
    state.setdefault("result", "")
    state.setdefault("plan", None)
    state.setdefault("current_task", None)
    state.setdefault("task_results", [])

    return state
