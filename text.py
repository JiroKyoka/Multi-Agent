from rag.loader import TextLoader
from rag.splitter import TextSplitter


loader=TextLoader(
    "paper.txt"
)


documents=loader.load()



splitter=TextSplitter(
    chunk_size=500
)


chunks=splitter.split(
    documents
)


print(len(chunks))