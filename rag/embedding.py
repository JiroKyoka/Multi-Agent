from abc import ABC, abstractmethod
from  sentence_transformers import SentenceTransformer
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_CACHE_DIR = PROJECT_ROOT / "models_cache"

class BaseEmbedding(ABC):

    @abstractmethod
    def embed(self, text):
        pass


class LocalEmbedding(BaseEmbedding):

    def __init__(self):
        self.model = SentenceTransformer("BAAI/bge-small-zh", cache_folder=str(MODEL_CACHE_DIR))

    def embed(self, text):
        return self.model.encode(text)