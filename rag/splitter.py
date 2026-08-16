from rag.document import Document

class TextSplitter:

    def __init__(self, chunk_size=500, overlap=50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, documents):

        chunks = []

        for doc in documents:
            text = doc.content

            start = 0

            while start < len(text):
                end = start + self.chunk_size
                chunk = text[start:min(end,len(text))]
                chunks.append(
                    Document(
                        content=chunk,
                        metadata={
                            **doc.metadata,
                            "start" : start,
                            "end" : end
                        }
                    )
                )
                start = end - self.overlap

        return chunks