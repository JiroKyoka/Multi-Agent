from tools.base import BaseTool

class RAGTool(BaseTool):
    def __init__(self, retriever, top_k=3):
        super().__init__(
            name="rag_search",
            description="当需要查询本地知识库或文档内容时使用",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "用于检索知识库的问题"
                    }
                },
                "required": ["query"]
            }
        )
        self.retriever = retriever
        self.top_k = top_k

    def run(self, query: str):
        documents = self.retriever.retrieve(query, top_k=self.top_k)
        return self.build_context(documents)

    def build_context(self, documents):
        parts = []

        for i, doc in enumerate(documents, start=1):
            parts.append(
                f"[参考资料{i}]\n"
                f"{doc.content}"
            )

        return "\n\n".join(parts)
