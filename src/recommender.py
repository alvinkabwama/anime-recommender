

import sys
from typing import Tuple, List

from langchain_classic.chains import RetrievalQA
from langchain_groq import ChatGroq
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from src.prompt_template import get_anime_prompt
from utils.custom_exception import CustomException
from utils.logger import logging


class AnimeRecommender:
    """
    High-level facade around a RetrievalQA chain that uses:
      - Chroma (or any retriever) for semantic search over anime data
      - ChatGroq as the LLM
      - A custom prompt for anime recommendations

    Usage:
        recommender = AnimeRecommender(retriever, api_key=..., model_name="mixtral-8x7b-32768")
        answer, sources = recommender.get_recommendation("cozy slice of life with found family")
    """

    def __init__(self, retriever: BaseRetriever, api_key: str, model_name: str, temperature: float = 0.0):
        """
        :param retriever: Any LangChain retriever (e.g. Chroma().as_retriever()).
        :param api_key:   GROQ API key.
        :param model_name:Groq model id (e.g. "mixtral-8x7b-32768").
        :param temperature:LLM temperature; 0.0 for deterministic answers.
        """
        self.retriever = retriever

        try:
            self.llm = ChatGroq(
                api_key=api_key,
                model=model_name,
                temperature=temperature,
            )
        except Exception as e:
            raise CustomException("Failed to initialize ChatGroq LLM", sys) from e

        # Your improved anime recommendation prompt
        self.prompt = get_anime_prompt()

        try:
            # Build a RetrievalQA chain:
            # 1) uses retriever to fetch docs
            # 2) stuffs them + question into the prompt
            # 3) sends that to the LLM
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.retriever,
                return_source_documents=True,
                chain_type_kwargs={"prompt": self.prompt},
                verbose=False,
            )
        except Exception as e:
            raise CustomException("Failed to create RetrievalQA chain", sys) from e

    def get_recommendation(self, query: str) -> str:
        """
        Run a recommendation query.

        :param query: Natural language description of what the user wants.
        :return: (result_text, source_documents)
        """
        try:
            # RetrievalQA expects a dict with key "query"
            result = self.qa_chain.invoke({"query": query})
            answer: str = result["result"]
            sources: List[Document] = result["source_documents"]

            logging.info("Anime recommendation generated successfully.")
            return answer
        except Exception as e:
            raise CustomException("Failed to generate anime recommendation", sys) from e
