from rag.embedding import LocalEmbedding
from rag.vectorstore import SimpleVectorStore
from rag.retriever import VectorRetriever
from rag.loader import TextLoader
from rag.splitter import TextSplitter

def init_rag(path:str):
    
    loader=TextLoader(path)

    documents=loader.load()

    splitter=TextSplitter()

    chunks=splitter.split(documents)

    embedding=LocalEmbedding()

    vectorstore=SimpleVectorStore(embedding)

    vectorstore.add(chunks)

    retriever=VectorRetriever(vectorstore)

    return retriever