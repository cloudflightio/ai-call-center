from loguru import logger

from vto_pipeline.exceptions import NoMatchError, NoProductsRecognizedError
from vto_pipeline.models.models import Item, OrderProposal, RecognizedProduct, UnmatchedItem
from vto_pipeline.services.entity_recognition import EntityRecognitionService
from vto_pipeline.services.search import SearchService
from vto_pipeline.util.text_utils import process_word_quantity


class OrderProposalService:
    def __init__(
        self,
        entity_recognition_service: EntityRecognitionService,
        search_service: SearchService,
    ):
        self.entity_recognizer = entity_recognition_service
        self.search = search_service

    def from_text(self, text: str) -> OrderProposal:
        products = self.entity_recognizer.extract_products(text)
        order = self._generate_order_proposal(products)
        return order

    def _generate_order_proposal(self, products: list[RecognizedProduct]) -> OrderProposal:
        if len(products) == 0:
            raise NoProductsRecognizedError

        order = OrderProposal(items=[])
        for p in products:
            item = self._find_item(p)
            order.items.append(item)

        logger.info(f"Order proposal: {order}")
        return order

    def _find_item(self, product: RecognizedProduct):
        quantity = process_word_quantity(product.quantity)
        try:
            match = self.search.find_match(product.product_identifier)
            return Item(
                quantity=quantity,
                unit=product.unit,
                sku=match.sku,
                product_name=match.product_name,
                speech=product.product_identifier,
            )
        except NoMatchError:
            logger.info("Replacing product without matches with an unmatched item object.")
            return UnmatchedItem(speech=product.product_identifier)
