import numpy as np
from rag.embedding import BaseEmbedding

class SimpleVectorStore: # 简易内存版向量数据库

    def __init__(self, embedding:BaseEmbedding):
        self.embedding = embedding
        self.vectors = []
        self.documents = []

    def add(self, documents:list):
        for doc in documents:
            vector = self.embedding.embed(doc.content)
            self.vectors.append(vector)
            self.documents.append(doc)

    def similarity(a,b):
        return np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))

    def search(self, query,top_k=3):
        query_vector = self.embedding.embed(query)

        scores = []

        for i,vector in enumerate(self.vectors):
            score = self.similarity(query_vector, vector)

            scores.append((score,i))

            scores.sort(reverse=True)

        results = []

        for score, index in scores[:top_k]:
            results.append(self.documents[index])

        return results