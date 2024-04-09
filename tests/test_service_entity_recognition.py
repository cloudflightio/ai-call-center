import pytest

from vto_pipeline.models.models import RecognizedProduct
from vto_pipeline.services.entity_recognition import FlairNerService, GptEntityRecognitionService


@pytest.mark.unit
def test_gpt_extract_products(gpt_ner_service: GptEntityRecognitionService):
    products = gpt_ner_service.extract_products("I want 5 bags of cheese")
    expected = [RecognizedProduct(product_identifier="cheese", unit="bags", quantity=5)]
    assert products == expected


@pytest.mark.unit
def test_flair_extract_products(flair_ner_service: FlairNerService):
    products = flair_ner_service.extract_products("I want 5 bags of cheese")
    expected = [
        RecognizedProduct(quantity="5", unit="bags", product_identifier="cheese"),
    ]
    assert products == expected
