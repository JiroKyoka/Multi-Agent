from typing import TypedDict, List
from core.message import Message
from core.task import TaskPlan

class AgentState(TypedDict):
    task : str                      # 用户的原始任务
    messages : List[Message]        # 上下文
    result : str                    # 最近一次agent的输出
    plan : TaskPlan | None          # planner agent的计划
    current_task : dict | None      # 子agent的任务，不同子任务送入的current_task不同
    task_results : List[dict]       # 子agent的任务结果，不同子任务得到的结果不同
    steps : List[dict]              # loop的执行日志
    errors : List[dict]             # 报错
    done : bool                     # 是否完成

def ensure_state_defaults(state: AgentState) -> AgentState:
    state.setdefault("task", "")
    state.setdefault("messages", [])
    state.setdefault("result", "")
    state.setdefault("plan", None)
    state.setdefault("current_task", None)
    state.setdefault("task_results", [])
    state.setdefault("steps", [])
    state.setdefault("errors", [])
    state.setdefault("done", False)

    return state
