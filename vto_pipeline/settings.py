from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class EntityRecognitionModel(str, Enum):
    flair = "flair"
    gpt = "gpt"


class LoggingSettings(BaseSettings):
    enabled: bool = True


class PipelineConfiguration(BaseSettings):
    entity_recognition_model: EntityRecognitionModel
    products_file: str


class AzureKeys(BaseSettings):
    azure_openai_key: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class AzureConfiguration(BaseSettings):
    openai_endpoint: str  # endpoint of the openai service (used for NER)
    openai_api_version: str  # version to be used for the openai service
    openai_deployment_name: str  # name of the model deployment (to be used for NER)


class FlairConfiguration(BaseSettings):
    final_model_file: str


class PipelineSettings(BaseSettings):
    pipeline: PipelineConfiguration
    logging: LoggingSettings

    flair: FlairConfiguration

    azure_keys: AzureKeys = AzureKeys()
    azure: AzureConfiguration
