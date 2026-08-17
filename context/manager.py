from context.token_counter import TokenCounter

class ContextManager:

    def __init__(
        self,
        token_counter :TokenCounter,
        max_context_tokens=12000,
        reserved_response_tokens=1500,
        memory_budget=1500,
        document_budget=4000
    ):
        self.token_counter = token_counter
        self.max_context_tokens = max_context_tokens
        self.reserved_response_tokens = reserved_response_tokens
        self.memory_budget = memory_budget
        self.document_budget = document_budget

    def select_memories(self, memories):
        selected = []
        used_tokens = 0

        for memory in reversed(memories):
            tokens = self.token_counter.count_text(
                memory.content
            )

            if (
                used_tokens + tokens
                > self.memory_budget
            ):
                continue

            selected.append(memory)
            used_tokens += tokens

        selected.reverse()

        return selected

    def select_documents(self, documents):
        selected = []
        used_tokens = 0

        for document in documents:
            tokens = self.token_counter.count_text(
                document.content
            )

            if (
                used_tokens + tokens
                > self.document_budget
            ):
                continue

            selected.append(document)
            used_tokens += tokens

        return selected

    def select_messages(
        self,
        messages,
        available_tokens
    ):
        selected = []
        used_tokens = 0

        for message in reversed(messages):
            tokens = self.token_counter.count_text(
                message.content
            )

            if (
                used_tokens + tokens
                > available_tokens
            ):
                continue

            selected.append(message)
            used_tokens += tokens

        selected.reverse()

        return selected

    def build_memory_text(
        self,
        memories
    ):
        if not memories:
            return ""

        parts = []

        for memory in memories:
            parts.append(
                f"- {memory.content}"
            )

        return "\n".join(parts)

    def build_document_text(
        self,
        documents
    ):
        if not documents:
            return ""

        parts = []

        for index, document in enumerate(
            documents,
            start=1
        ):
            parts.append(
                f"[参考资料{index}]\n"
                f"{document.content}"
            )

        return "\n\n".join(parts)

    def build(
        self,
        system_prompt,
        messages,
        memories,
        documents
    ):
        selected_memories = ( # 获取预先规定的token数量的记忆
            self.select_memories(
                memories
            )
        )

        selected_documents = ( # 获取预先规定的token数量的rag检索文献
            self.select_documents(
                documents
            )
        )

        memory_text = ( # 整合记忆成为一个大字符串
            self.build_memory_text(
                selected_memories
            )
        )

        document_text = ( # 整合rag数据成一个大字符串
            self.build_document_text(
                selected_documents
            )
        )

        system_tokens = ( # 计算系统提示词的token
            self.token_counter.count_text(
                system_prompt
            )
        )

        memory_tokens = ( # 计算记忆的token
            self.token_counter.count_text(
                memory_text
            )
        )

        document_tokens = ( # 计算数据库的token
            self.token_counter.count_text(
                document_text
            )
        )

        input_budget = ( # 计算输入
            self.max_context_tokens
            - self.reserved_response_tokens
        )

        message_budget = (
            input_budget
            - system_tokens
            - memory_tokens
            - document_tokens
        )

        message_budget = max( # 计算剩余token预算
            message_budget,
            0
        )

        selected_messages = ( # 获取最大上文message
            self.select_messages(
                messages,
                message_budget
            )
        )

        final_messages = [ # 开始整合message
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        if memory_text:
            final_messages.append(
                {
                    "role": "system",
                    "content":
                        "以下是长期记忆：\n\n"
                        f"{memory_text}"
                }
            )

        if document_text:
            final_messages.append(
                {
                    "role": "system",
                    "content":
                        "以下是与当前任务相关的"
                        "知识库资料：\n\n"
                        f"{document_text}"
                }
            )

        for message in selected_messages:
            final_messages.append(
                {
                    "role": message.role,
                    "content": message.content
                }
            )

        return final_messages