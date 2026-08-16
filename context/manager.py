class ContextManager:

    def __init__(
        self,
        max_messages=10,
        max_memories=5,
        max_documents=3
    ):
        self.max_messages = max_messages

        self.max_memories = max_memories

        self.max_documents = max_documents

    def select_messages(
        self,
        messages
    ):
        return messages[
            -self.max_messages:
        ]

    def select_memories(
        self,
        memories
    ):
        return memories[
            -self.max_memories:
        ]

    def select_documents(
        self,
        documents
    ):
        return documents[
            :self.max_documents
        ]