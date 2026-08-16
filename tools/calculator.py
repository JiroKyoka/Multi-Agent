from tools.base import BaseTool

class CalculatorTool(BaseTool):

    def __init__(self, name="calculator", description="用于数学计算"):
        super().__init__(name, description, parameters={
            "type":"object",
            "properties":{
                "experssion":{
                    "type":"string",
                    "description":"数学表达式"
                }
            },
            "required":["experssion"]
        })

    def run(self, experssion):
        return str(eval(experssion))