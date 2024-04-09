from abc import ABC, abstractmethod

from flair.models import SequenceTagger

from vto_pipeline.clients.azure_openai import AzureOpenaiClient
from vto_pipeline.models.models import RecognizedProduct


class EntityRecognitionService(ABC):
    @abstractmethod
    def extract_products(self, text: str) -> list[RecognizedProduct]:
        pass


class FlairNerService(EntityRecognitionService):
    def __init__(self, model_file: str):
        self.model = SequenceTagger.load(model_file)

    def extract_products(self, text: str) -> list[RecognizedProduct]:
        # TODO: Implement this method for Ticket 1
        pass


class GptEntityRecognitionService:
    def __init__(self, azure_openai_client: AzureOpenaiClient):
        self.azure_openai_client = azure_openai_client

    def extract_products(self, order_message: str) -> list[RecognizedProduct]:
        # TODO: Implement this method for Ticket 1
        pass
