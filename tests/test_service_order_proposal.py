import pytest

from vto_pipeline.models.models import Item, RecognizedProduct
from vto_pipeline.services.order_generation import OrderProposalService


@pytest.mark.unit
def test_from_text(order_proposal_service: OrderProposalService):
    order_proposal = order_proposal_service.from_text("Testing order generation", "taskid")

    assert order_proposal.items


@pytest.mark.unit
def test_find_items(order_proposal_service: OrderProposalService):
    product = RecognizedProduct(quantity=5, unit="default", product_identifier="Milk")
    item = order_proposal_service._find_item(product)

    expected = Item(quantity=5, unit="default", sku="0000", product_name="mocked product", speech="Milk")
    assert item == expected
