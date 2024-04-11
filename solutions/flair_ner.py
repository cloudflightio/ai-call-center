import string
from functools import lru_cache

from flair.data import Sentence, Span
from flair.models import SequenceTagger
from loguru import logger

from vto_pipeline.models.entity_group import EntityGroup
from vto_pipeline.models.models import Entity, EntityType, RecognizedProduct
from vto_pipeline.util.text_utils import find_entity_groups


class FlairEntityRecognitionService:
    def __init__(self, model_file: str):
        self.model = SequenceTagger.load(model_file)

    def extract_products(self, text: str) -> list[RecognizedProduct]:
        logger.info("Product recognition started using NER model to extract entities from text.")

        entities = self._extract_entities(text)

        product_entities = self._filter_product_entities(entities)
        groups: list[EntityGroup] = find_entity_groups(product_entities)
        return [g.to_recognized_product() for g in groups]

    @staticmethod
    def _filter_product_entities(entities: list[Entity]) -> list[Entity]:
        return [e for e in entities if e.category is not EntityType.OTHER]

    @lru_cache
    def _extract_entities(self, text: str):
        text = text.lower().translate(str.maketrans("", "", string.punctuation))
        sentence = Sentence(text)
        try:
            self.model.predict(sentence)
            return sentence.get_spans()
        except Exception as err:
            logger.error("Encountered exception. {}".format(err))

        return self._format_results()

    @staticmethod
    def _format_results(spans: list[Span]) -> list[Entity]:
        return [Entity.from_span(span) for span in spans]
