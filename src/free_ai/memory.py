import logging
import os
import chromadb
import uuid
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class VectorMemory:
    def __init__(self, path="./collective_memory_db"):
        """
        Initializes the VectorMemory, the agent society's persistent, shared memory.
        Uses ChromaDB for storage and SentenceTransformers for embeddings.
        """
        logger.info(f"Initializing VectorMemory at path: {path}")
        try:
            self.client = chromadb.PersistentClient(path=path)
            model_cache_path = os.path.join(path, "st_cache")
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu', cache_folder=model_cache_path)
            self.collection_name = "collective_unconscious"
            self.collection = self.client.get_or_create_collection(name=self.collection_name)
            logger.info(f"VectorMemory initialized. Collective Unconscious '{self.collection_name}' is online.")
        except Exception as e:
            logger.error(f"Failed to initialize VectorMemory: {e}", exc_info=True)
            raise

    def add(self, text: str, metadata: dict = None):
        """
        Adds a piece of text to the collective memory.
        The text is converted into an embedding and stored with a unique ID.
        """
        try:
            logger.info(f"Adding text to collective memory: '{text[:50]}...'")
            embedding = self.embedding_model.encode(text).tolist()
            doc_id = str(uuid.uuid4())

            # ChromaDB requires metadata to be a non-empty dict.
            final_metadata = metadata if metadata else {"source": "unknown", "timestamp": str(uuid.uuid4())}

            self.collection.add(
                embeddings=[embedding],
                documents=[text],
                metadatas=[final_metadata],
                ids=[doc_id]
            )
            logger.info(f"Successfully added document with ID {doc_id} to collective memory.")
        except Exception as e:
            logger.error(f"Failed to add text to collective memory: {e}", exc_info=True)


    def query(self, query_text: str, n_results: int = 3) -> list[str]:
        """
        Searches the collective memory for text semantically similar to the query_text.
        """
        try:
            logger.info(f"Querying collective memory with: '{query_text[:50]}...'")
            if self.collection.count() == 0:
                logger.warning("Query attempted on an empty collection.")
                return []

            query_embedding = self.embedding_model.encode(query_text).tolist()

            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=min(n_results, self.collection.count()) # Ensure n_results <= collection count
            )

            retrieved_docs = results.get('documents', [[]])[0]
            logger.info(f"Query returned {len(retrieved_docs)} results from collective memory.")
            return retrieved_docs
        except Exception as e:
            logger.error(f"Failed to query collective memory: {e}", exc_info=True)
            return []

    def clear(self):
        """Clears all memories from the collection."""
        logger.warning(f"Clearing all documents from collection '{self.collection_name}'.")
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.get_or_create_collection(name=self.collection_name)
        logger.info(f"Collection '{self.collection_name}' has been cleared and recreated.")