from agents.base_agent import BaseAgent
from models.llm import ChatLLM
from core.message import Message
from rag.retriever import BaseRetriever
from memory.store import SQLiteMemoryStore
from context.manager import ContextManager

class RAGAgent(BaseAgent):

    def __init__(self, name="rag_agent", retriever: BaseRetriever=None, context_manager: ContextManager=None, memory_store: SQLiteMemoryStore=None):
        super().__init__(name)
        self.llm = ChatLLM()
        self.retriever = retriever
        self.context_manager = context_manager
        self.memory_store = memory_store

    def run(self, state):

        current_task = state["current_task"]


        query = current_task["description"] # 此处还没有规定子任务的字典构成


        documents = self.retriever.retrieve(query, 3)
        memories = self.memory_store.list_all()
        messages = self.context_manager.build(
            system_prompt="你是一个知识检索与分析Agent，请根据知识库资料完成当前子任务",
            messages=state["messages"],
            memories=memories,
            documents=documents
        )
        messages.append({
            "role": "user",
            "content": "query"
        })

        response = self.llm.invoke(messages)

        result = response.content

        state["task_results"].append( # 此处还没规定子任务结果的构成字典
            {
                "task": current_task["name"],
                "agent": self.name,
                "result": result
            }
        )

        return state


