import pytest

from vto_pipeline.clients.azure_openai import AzureOpenaiClient
from vto_pipeline.models.models import ChatgptMessage, ChatgptRole


@pytest.mark.integration
def test_complete_chat(azure_openai_client: AzureOpenaiClient):
    chatgpt_message = ChatgptMessage(role=ChatgptRole.user, content="Testing if chatgpt works")
    response = azure_openai_client.complete_chat([chatgpt_message])
    assert response.startswith("Hello!")
