import re


class TokenCounter:

    def count_text(self, text: str) -> int:
        if not text:
            return 0

        chinese_chars = re.findall(
            r"[\u4e00-\u9fff]",
            text
        )

        non_chinese = re.sub(
            r"[\u4e00-\u9fff]",
            "",
            text
        )

        chinese_tokens = len(chinese_chars)

        english_tokens = max(
            0,
            len(non_chinese) // 4
        )

        return chinese_tokens + english_tokens

    def count_messages(self, messages) -> int:
        total = 0

        for message in messages:
            total += self.count_text(
                message.content
            )

        return total

    def count_documents(self, documents) -> int:
        total = 0

        for document in documents:
            total += self.count_text(
                document.content
            )

        return total

    def count_memories(self, memories) -> int:
        total = 0

        for memory in memories:
            total += self.count_text(
                memory.content
            )

        return total