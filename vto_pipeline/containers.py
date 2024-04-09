from pathlib import Path

from dependency_injector import containers, providers

from vto_pipeline.clients.azure_openai import AzureOpenaiClient
from vto_pipeline.services.entity_recognition import (
    EntityRecognitionService,
    FlairNerService,
    GptEntityRecognitionService,
)
from vto_pipeline.services.order_generation import OrderProposalService
from vto_pipeline.services.search import SearchService
from vto_pipeline.settings import PipelineSettings

P = providers.Provider

packages = ["vto_pipeline"]
if Path("./tests").is_dir():
    packages.append("tests")  # pragma: no cover


class Pipeline(containers.DeclarativeContainer):
    settings: PipelineSettings = providers.Configuration()
    wiring_config = containers.WiringConfiguration(packages=packages)

    openai_client: P[AzureOpenaiClient] = providers.Singleton(
        AzureOpenaiClient,
        key=settings.azure_keys.azure_openai_key,
        endpoint=settings.azure.openai_endpoint,
        api_version=settings.azure.openai_api_version,
        deployment_name=settings.azure.openai_deployment_name,
    )

    # Entity recognition component:
    entity_recognition_service: P[EntityRecognitionService] = providers.Selector(
        settings.pipeline.entity_recognition_model,
        flair=providers.Singleton(FlairNerService, model_file=settings.flair.final_model_file),
        gpt=providers.Singleton(
            GptEntityRecognitionService,
            azure_openai_client=openai_client,
        ),
    )

    search_service: P[SearchService] = providers.Singleton(
        SearchService, products_file=settings.pipeline.products_file
    )

    # Order generation component, using all the components above:
    order_proposal_service: P[OrderProposalService] = providers.Singleton(
        OrderProposalService,
        entity_recognition_service=entity_recognition_service,
        search_service=search_service,
    )
