from typing import Generator

import pytest

from vto_pipeline import load_settings
from vto_pipeline.clients.azure_openai import AzureOpenaiClient
from vto_pipeline.containers import Pipeline
from vto_pipeline.services.entity_recognition import FlairNerService, GptEntityRecognitionService
from vto_pipeline.services.order_generation import OrderProposalService
from vto_pipeline.services.search import SearchService


@pytest.fixture
def test_container() -> Pipeline:
    return setup_pipeline_container("config.yaml")


def setup_pipeline_container(yaml_file: str) -> Pipeline:
    container = Pipeline()
    settings = load_settings(yaml_file)
    container.settings.from_dict(settings.model_dump())
    container.wire()
    return container


# -------------- CLIENTS


@pytest.fixture
def azure_openai_client(test_container: Pipeline) -> Generator[AzureOpenaiClient, None, None]:
    yield test_container.openai_client()
    test_container.reset_singletons()


# -------------- SERVICES


@pytest.fixture
def gpt_ner_service(test_container: Pipeline) -> Generator[GptEntityRecognitionService, None, None]:
    yield test_container.entity_recognition_service()
    test_container.reset_singletons()


@pytest.fixture
def flair_ner_service(test_container: Pipeline) -> Generator[FlairNerService, None, None]:
    yield test_container.entity_recognition_service()
    test_container.reset_singletons()


@pytest.fixture
def search_service(
    test_container: Pipeline,
) -> Generator[SearchService, None, None]:
    yield test_container.search_service()
    test_container.reset_singletons()


@pytest.fixture
def order_proposal_service(
    test_container: Pipeline,
) -> Generator[OrderProposalService, None, None]:
    yield test_container.order_proposal_service()
    test_container.reset_singletons()
