import logging
import chromadb
import uuid
import os

# The sentence-transformers library will be downloaded on first use.
# This is a one-time cost.
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class VectorMemory:
    def __init__(self, path="./memory_db"):
        """
        Initializes the VectorMemory, the agent's persistent, long-term memory.
        Uses ChromaDB for storage and SentenceTransformers for embeddings.
        """
        logger.info(f"Initializing VectorMemory at path: {path}")
        try:
            self.client = chromadb.PersistentClient(path=path)
            # Specify cache_folder to control where models are downloaded.
            model_cache_path = os.path.join(path, "st_cache")
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu', cache_folder=model_cache_path)
            self.collection_name = "agent_knowledge"
            self.collection = self.client.get_or_create_collection(name=self.collection_name)
            logger.info(f"VectorMemory initialized. Collection '{self.collection_name}' ready.")
        except Exception as e:
            logger.error(f"Failed to initialize VectorMemory: {e}", exc_info=True)
            raise

    def add(self, text: str, metadata: dict = None):
        """
        Adds a piece of text to the memory.
        The text is converted into an embedding and stored with a unique ID.
        """
        try:
            logger.info(f"Adding text to memory: '{text[:50]}...'")
            embedding = self.embedding_model.encode(text).tolist()
            doc_id = str(uuid.uuid4())

            # ChromaDB requires metadata to be a non-empty dict.
            # We'll use the provided metadata or create a default one.
            final_metadata = metadata if metadata else {"source": "unknown", "timestamp": str(uuid.uuid4())}

            self.collection.add(
                embeddings=[embedding],
                documents=[text],
                metadatas=[final_metadata],
                ids=[doc_id]
            )
            logger.info(f"Successfully added document with ID {doc_id} to memory.")
        except Exception as e:
            logger.error(f"Failed to add text to memory: {e}", exc_info=True)


    def query(self, query_text: str, n_results: int = 3) -> list[str]:
        """
        Searches the memory for text semantically similar to the query_text.
        """
        try:
            logger.info(f"Querying memory with: '{query_text[:50]}...'")
            if self.collection.count() == 0:
                logger.warning("Query attempted on an empty collection.")
                return []

            query_embedding = self.embedding_model.encode(query_text).tolist()

            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )

            # The results contain a list of documents, we want the first list inside.
            retrieved_docs = results.get('documents', [[]])[0]
            logger.info(f"Query returned {len(retrieved_docs)} results.")
            return retrieved_docs
        except Exception as e:
            logger.error(f"Failed to query memory: {e}", exc_info=True)
            return []

    def clear(self):
        """Clears all memories from the collection."""
        logger.warning(f"Clearing all documents from collection '{self.collection_name}'.")
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.get_or_create_collection(name=self.collection_name)
        logger.info(f"Collection '{self.collection_name}' has been cleared and recreated.")