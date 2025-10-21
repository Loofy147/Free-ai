import logging
import os
import chromadb
import uuid
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class VectorMemory:
    """A persistent, semantic memory store for agents using vector embeddings.

    This class provides a long-term memory solution for agents by converting
    text into vector embeddings and storing them in a ChromaDB database. This
    allows for efficient semantic search, enabling agents to recall relevant
    information based on meaning rather than keywords.

    Attributes:
        client: The ChromaDB client instance.
        embedding_model: The SentenceTransformer model used for embeddings.
        collection_name (str): The name of the ChromaDB collection.
        collection: The ChromaDB collection object.
    """

    def __init__(self, path="./collective_memory_db"):
        """Initializes the VectorMemory database.

        Sets up a persistent ChromaDB client at the specified path and
        initializes the sentence-transformer model for creating embeddings.

        Args:
            path (str): The file system path to store the database.
        """
        logger.info(f"Initializing VectorMemory at path: {path}")
        try:
            self.client = chromadb.PersistentClient(path=path)
            model_cache_path = os.path.join(path, "st_cache")
            self.embedding_model = SentenceTransformer(
                "all-MiniLM-L6-v2", device="cpu", cache_folder=model_cache_path
            )
            self.collection_name = "collective_unconscious"
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name
            )
            logger.info(
                f"VectorMemory initialized. Collective Unconscious '{self.collection_name}' is online."
            )
        except Exception as e:
            logger.error(f"Failed to initialize VectorMemory: {e}", exc_info=True)
            raise

    def add(self, text: str, metadata: dict = None):
        """Adds a text document to the vector memory.

        The text is encoded into a vector embedding and stored in the
        ChromaDB collection along with a unique ID and optional metadata.

        Args:
            text (str): The text content to add to the memory.
            metadata (dict, optional): A dictionary of metadata to associate
                with the text. Defaults to None.
        """
        try:
            logger.info(f"Adding text to collective memory: '{text[:50]}...'")
            embedding = self.embedding_model.encode(text).tolist()
            doc_id = str(uuid.uuid4())

            # ChromaDB requires metadata to be a non-empty dict.
            final_metadata = (
                metadata
                if metadata
                else {"source": "unknown", "timestamp": str(uuid.uuid4())}
            )

            self.collection.add(
                embeddings=[embedding],
                documents=[text],
                metadatas=[final_metadata],
                ids=[doc_id],
            )
            logger.info(
                f"Successfully added document with ID {doc_id} to collective memory."
            )
        except Exception as e:
            logger.error(f"Failed to add text to collective memory: {e}", exc_info=True)

    def query(self, query_text: str, n_results: int = 3) -> list[str]:
        """Performs a semantic search on the vector memory.

        Encodes the query text into an embedding and searches the collection
        for the most semantically similar documents.

        Args:
            query_text (str): The text to search for.
            n_results (int): The maximum number of results to return.

        Returns:
            list[str]: A list of the most relevant document texts found.
        """
        try:
            logger.info(f"Querying collective memory with: '{query_text[:50]}...'")
            if self.collection.count() == 0:
                logger.warning("Query attempted on an empty collection.")
                return []

            query_embedding = self.embedding_model.encode(query_text).tolist()

            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=min(
                    n_results, self.collection.count()
                ),  # Ensure n_results <= collection count
            )

            retrieved_docs = results.get("documents", [[]])[0]
            logger.info(
                f"Query returned {len(retrieved_docs)} results from collective memory."
            )
            return retrieved_docs
        except Exception as e:
            logger.error(f"Failed to query collective memory: {e}", exc_info=True)
            return []

    def clear(self):
        """Clears all documents from the memory collection.

        This deletes and recreates the collection, effectively wiping all
        stored memories.
        """
        logger.warning(
            f"Clearing all documents from collection '{self.collection_name}'."
        )
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name
        )
        logger.info(
            f"Collection '{self.collection_name}' has been cleared and recreated."
        )
