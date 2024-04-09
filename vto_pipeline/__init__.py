from pathlib import Path

import yaml

from vto_pipeline.containers import Pipeline
from vto_pipeline.settings import PipelineSettings


def load_settings(yaml_file: str) -> PipelineSettings:
    yaml_file_path = Path(__file__).parent.parent / "config" / yaml_file
    config: dict = {}
    with open(yaml_file_path, "r") as config_yaml:
        config.update(yaml.safe_load(config_yaml))
    return PipelineSettings(**config)


def generate_pipeline(settings: PipelineSettings) -> Pipeline:
    container = Pipeline()
    container.settings.from_dict(settings.model_dump())
    return container
