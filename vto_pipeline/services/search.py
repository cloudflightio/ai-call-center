import json

from loguru import logger
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import semantic_search

from vto_pipeline.models.models import Match


class SearchService:
    def __init__(self, products_file: str):
        """Initialize the semantic search service"""
        self.model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

        with open(products_file) as data:
            self.products = json.load(data)

        names = [product["name"] for product in self.products]
        self.product_embeddings = self.model.encode(names)

    def find_match(self, product_identifier: str) -> Match:
        """Use the semantic search engine to match the identified product to an article."""
        logger.info("Searching for product...")

        query = self.model.encode(product_identifier)
        k = len(self.product_embeddings)
        matches = semantic_search(
            query, self.product_embeddings, query_chunk_size=1, corpus_chunk_size=k, top_k=2
        )

        product = self.products[matches[0][0]["corpus_id"]]
        return Match(
            product_name=product["name"], product_category="0", sku=str(product["sku"]), full_result=matches
        )
