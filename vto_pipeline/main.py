from dependency_injector.wiring import Provide, inject
from loguru import logger

from vto_pipeline import generate_pipeline, load_settings
from vto_pipeline.containers import Pipeline
from vto_pipeline.exceptions import OrderGenerationError
from vto_pipeline.services.order_generation import OrderProposalService
from vto_pipeline.util.text_utils import load_example_order


@inject
def main(
    order_generator: OrderProposalService = Provide[Pipeline.order_proposal_service],
):
    logger.info("Running the pipeline for a random order example from the dataset.")
    try:
        text, _ = load_example_order()
        logger.info(f"Order message: {text}")
        order_proposal = order_generator.from_text(text)
        logger.info(f"Order proposal generated: {order_proposal}")
    except OrderGenerationError as error:
        logger.error(f"An error occurred during order generation for text '{text}'.")
        raise error


if __name__ == "__main__":
    settings = load_settings("config.yaml")
    container = generate_pipeline(settings)
    container.wire(modules=[__name__])
    main()
