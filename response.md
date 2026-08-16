response = {
    "id": "chatcmpl-xxx",
    "object": "chat.completion",
    "created": 1741570283,
    "model": "gpt-4o-xxx",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "模型回复的正文"
                "tool_calls": [
                    {
                        "id": "call_xxx"        # 后面你把工具执行结果发回给模型时，要用这个 ID 对上是哪一次工具调用的结果。
                        "type": "function"      # 工具调用类型
                        "function": {
                            "name": "函数名字"
                            "arguments": "{\"参数名字\": \"参数\"}"
                        }
                    }
                ]
            },
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 100,
        "completion_tokens": 50,
        "total_tokens": 150
    }
}

{
    "role": "tool",
    "tool_call_id": "call_abc123",
    "content": "搜索结果..."
}