# pipeline.py
import sys
from typing import Tuple, List

from langchain_core.documents import Document

from src.vector_store import VectorStoreBuilder
from src.recommender import AnimeRecommender
from utils.logger import get_logger
from utils.custom_exception import CustomException
from config.config import (GROQ_API_KEY, GROQ_MODEL_NAME)

logger = get_logger(__name__)


class AnimeRecommendationPipeline:
    """
    Orchestrates the full anime recommendation flow:

    1. Loads (or builds) a Chroma vector store from a processed CSV.
    2. Creates a retriever from that vector store.
    3. Wires the retriever into an AnimeRecommender (ChatGroq + custom prompt).
    4. Exposes a simple `recommend(query)` method for external callers.
    """

    def __init__(self, csv_path: str, persist_dir: str = "chroma_db", build_if_missing: bool = False):
        """
        :param csv_path: Path to the processed CSV with `combined_info` column.
        :param persist_dir: Directory where Chroma DB is stored.
        :param build_if_missing: If True, call `build_and_save_vectorstore()` before loading.
        """
        try:
            logger.info(
                "Initializing AnimeRecommendationPipeline with csv_path=%s, persist_dir=%s",
                csv_path,
                persist_dir,
            )

            # 1. Create vector builder
            self.vector_builder = VectorStoreBuilder(csv_path=csv_path, persist_dir=persist_dir)

            # Optionally build the vector store (e.g. on first run / offline job)
            if build_if_missing:
                logger.info("Building and persisting Chroma vector store...")
                self.vector_builder.build_and_save_vectorstore()

            # 2. Load vector store and create retriever
            vector_store = self.vector_builder.load_vectorstore()
            retriever = vector_store.as_retriever()
            logger.info("Vector store loaded and retriever created successfully.")

            # 3. Create the high-level recommender
            self.recommender = AnimeRecommender(
                retriever=retriever,
                api_key=GROQ_API_KEY,
                model_name=GROQ_MODEL_NAME,
                temperature=0.0,
            )
            logger.info("AnimeRecommender initialized successfully.")

        except Exception as e:
            logger.error("Error initializing AnimeRecommendationPipeline", exc_info=True)
            # Wrap in your CustomException with file + line info
            raise CustomException("Error initializing AnimeRecommendationPipeline", sys) from e

    def recommend(self, query: str) -> str:
        """
        Run the full recommendation pipeline.

        :param query: Natural language description of what the user wants.
        :return: (answer_text, source_documents)
        """
        try:
            logger.info("Received recommendation query: %s", query)
            answer = self.recommender.get_recommendation(query)
            logger.info("Recommendation generated successfully.")
            return answer

        except Exception as e:
            logger.error("Failed to get recommendation", exc_info=True)
            raise CustomException("Failed to get recommendation", sys) from e
