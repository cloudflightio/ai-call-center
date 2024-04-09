from openai import AzureOpenAI

from vto_pipeline.models.models import ChatgptMessage


class MockAzureOpenaiClient:
    def complete_chat(self, chat_to_complete: list[ChatgptMessage]) -> str:
        return """[{'product_identifier': 'salzburg milch frischk\u00e4se kr\u00e4uter', 'quantity': 9,
                    'unit': ' k\u00fcbel'}, {'product_identifier': 'rupp haferflocken 5kg', 'quantity': 2,
                    'unit': 'default'}]"""


class AzureOpenaiClient:
    def __init__(self, key: str, endpoint: str, api_version: str, deployment_name: str):
        self.client = AzureOpenAI(api_key=key, api_version=api_version, azure_endpoint=endpoint)
        self.model = deployment_name

    def complete_chat(self, chat_to_complete: list[ChatgptMessage]) -> str:
        """Chat completion is a way to get ChatGPT to create desired behavior."""
        chat_to_complete = [m.model_dump() for m in chat_to_complete]  # map to dicts
        response = self.client.chat.completions.create(model=self.model, messages=chat_to_complete)
        return response.choices[0].message.content
