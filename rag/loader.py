from rag.document import Document

class TextLoader:

    def __init__(self, path):
        self.path = path

    def load(self):
        with open(self.path, "r", encoding="utf-8") as f:
            text = f.read()

        return [Document(content=text, metadata={"source":self.path})]