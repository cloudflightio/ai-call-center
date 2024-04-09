import pytest

from vto_pipeline.services.search import SearchService


@pytest.mark.unit
def test_find_match(search_service: SearchService):
    product_text = "Cloudflight Käse"
    result = search_service.find_match(product_text)
    expected_sku = "9282"
    assert result.sku == expected_sku
