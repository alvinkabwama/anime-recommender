# src/vector_store.py
import sys
from pathlib import Path
from dotenv import load_dotenv

from utils.logger import logging
from utils.custom_exception import CustomException
from config.config import (
    HUGGINGFACE_MODEL_NAME,
    HUGGINGFACE_MODEL_CACHE_DIR,
)

from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()


class VectorStoreBuilder:
    """
    Builds and persists a Chroma vector store from a processed CSV that contains a
    `combined_info` column. Also supports reloading the persisted store.
    """

    def __init__(self, csv_path: str, persist_dir: str = "chroma_db", collection: str = "anime"):
        self.csv_path = csv_path
        self.persist_dir = persist_dir
        self.collection = collection

        try:
            cache_dir: Path = HUGGINGFACE_MODEL_CACHE_DIR
            cache_dir.mkdir(parents=True, exist_ok=True)

            if any(cache_dir.iterdir()):
                logging.info(f"HF cache directory exists and is not empty: {cache_dir}")
            else:
                logging.info(
                    f"HF cache directory is empty: {cache_dir}. "
                    f"Model '{HUGGINGFACE_MODEL_NAME}' will be downloaded on first use."
                )

            # ✅ use cache_folder here, no model_kwargs
            self.embedding = HuggingFaceEmbeddings(
                model_name=HUGGINGFACE_MODEL_NAME,
                cache_folder=str(cache_dir),
                encode_kwargs={"normalize_embeddings": True},
                # local_files_only=True,  # optional offline mode
            )
            logging.info(f"HuggingFaceEmbeddings initialized with model: {HUGGINGFACE_MODEL_NAME}")

        except Exception as e:
            raise CustomException("Failed to initialize embedding model", sys) from e

    def build_and_save_vectorstore(self) -> None:
        if not Path(self.csv_path).exists():
            raise CustomException(f"Processed CSV not found: {self.csv_path}", sys)

        try:
            loader = CSVLoader(
                file_path=self.csv_path,
                encoding="utf-8",
                source_column="combined_info",
                metadata_columns=[],
            )
            docs = loader.load()
        except Exception as e:
            raise CustomException("Failed to load documents from CSV", sys) from e

        if not docs:
            raise CustomException("No documents were loaded from the processed CSV", sys)

        try:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=100,
                separators=["\n\n", "\n", ". ", " ", ""],
            )
            chunks = splitter.split_documents(docs)
        except Exception as e:
            raise CustomException("Failed to split documents into chunks", sys) from e

        if not chunks:
            raise CustomException("No chunks were produced by the text splitter", sys)

        try:
            db = Chroma.from_documents(
                documents=chunks,
                embedding=self.embedding,
                persist_directory=self.persist_dir,
                collection_name=self.collection,
            )
            db.persist()
            logging.info(
                f"Chroma vector store saved at {self.persist_dir} "
                f"(collection='{self.collection}')"
            )
        except Exception as e:
            raise CustomException("Failed to build or persist Chroma vector store", sys) from e

    def load_vectorstore(self) -> Chroma:
        try:
            return Chroma(
                collection_name=self.collection,
                persist_directory=self.persist_dir,
                embedding_function=self.embedding,
            )
        except Exception as e:
            raise CustomException("Failed to load persisted Chroma vector store", sys) from e
