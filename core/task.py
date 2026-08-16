from dataclasses import dataclass
from typing import List

@dataclass
class Task:
    name:str # 任务名字
    agent:str # agent名字
    description:str # 任务描述

@dataclass
class TaskPlan:
    tasks:List[Task]