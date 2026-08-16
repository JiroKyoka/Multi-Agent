from rag.base import BaseRetriever

class SimpleRetriever(BaseRetriever): # 简易内存版本，直接读取前几条

    def __init__(self):

        self.documents=[]

    def add(
        self,
        text
    ):

        self.documents.append(text)

    def retrieve(
        self,
        query,
        top_k=3
    ):

        return self.documents[:top_k]

class VectorRetriever: # 向量内存版，匹配向量相似度最高的


    def __init__(
        self,
        vectorstore
    ):

        self.vectorstore=vectorstore



    def retrieve(
        self,
        query,
        top_k=3
    ):

        return self.vectorstore.search(
            query,
            top_k
        )