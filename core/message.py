from typing import Literal
from dataclasses import dataclass

@dataclass
class Message:

    role : Literal[
        "system",
        "user",
        "assistant",
        "tool"
    ]
    # 限制role只能在这四个里面选择
    tool_call_id : str = None
    content : str = None