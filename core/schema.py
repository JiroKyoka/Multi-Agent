from tools.base import BaseTool

def tool_schema(tool:BaseTool):

    return {
        "type":"function",

        "function":{

            "name":tool.name,

            "description":tool.description,

            "parameters":tool.parameters

        }
    }

