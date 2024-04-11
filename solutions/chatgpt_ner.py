import ast

from loguru import logger

from vto_pipeline.clients.azure_openai import AzureOpenaiClient
from vto_pipeline.exceptions import ChatGPTResponseProcessingError
from vto_pipeline.models.models import ChatgptMessage, ChatgptRole, RecognizedProduct


class GptEntityRecognitionService:
    def __init__(self, azure_openai_client: AzureOpenaiClient):
        self.azure_openai_client = azure_openai_client

    def _create_product_recognition_instructions(self, voice_message: str):
        """Set up the example chat to sent to ChatGPT. Its task will be to provide the next assistant message."""

        system_message = ChatgptMessage(
            role=ChatgptRole.system,
            content="""You are a helpful assistant trained to recognize products that German customers want
                                to order. The products are always associated with a quantity and sometimes a specific
                                packing unit. Configure your output as a list of valid python dicts. Each product
                                should have 3 entries: product_identifier, quantity and unit. If the unit is not
                                specified, set it to 'default'.""",
        )
        user_example_request = ChatgptMessage(
            role=ChatgptRole.user,
            content="""Recognize the products mentioned in the following transcription of a voice message:
                                'Bitte f\u00fcgen Sie zu meiner Bestellung 9 k\u00fcbel salzburg milch frischk\u00e4se
                                kr\u00e4uter und 3 mal rupp haferflocken 5kg hinzu.'""",
        )
        assistent_example_response = ChatgptMessage(
            role=ChatgptRole.assistant,
            content="""[{'product_identifier': 'salzburg milch frischk\u00e4se kr\u00e4uter', 'quantity': 9,
                                'unit': ' k\u00fcbel'}, {'product_identifier': 'rupp haferflocken 5kg', 'quantity': 2,
                                'unit': 'default'}]""",
        )
        user_ner_request = ChatgptMessage(
            role=ChatgptRole.user,
            content=f"""Recognize the products mentioned in the following transcription of a voice message:
                                '{voice_message}'""",
        )
        return [system_message, user_example_request, assistent_example_response, user_ner_request]

    def extract_products(self, order_message: str) -> list[RecognizedProduct]:
        logger.info("Product recognition started using ChatGPT to extract entities from text.")

        request_entities_chat = self._create_product_recognition_instructions(order_message)
        entities = self.azure_openai_client.complete_chat(request_entities_chat)
        logger.info(f"ChatGPT response: {entities}")
        return self._format_response(entities)

    @staticmethod
    def _format_response(response: str) -> list[RecognizedProduct]:
        """Extract a list of dictionaries from the chatGPT response."""
        products_list = ast.literal_eval(response)
        if not (isinstance(products_list, list) and all(isinstance(item, dict) for item in products_list)):
            raise ChatGPTResponseProcessingError(response)

        return [
            RecognizedProduct(
                quantity=p["quantity"], unit=p["unit"], product_identifier=p["product_identifier"]
            )
            for p in products_list
        ]
