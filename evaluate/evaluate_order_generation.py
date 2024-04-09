from loguru import logger
from utils import evaluate_text_to_order, print_results

from vto_pipeline import generate_pipeline, load_settings


def evaluate_model(data_folder: str):
    settings = load_settings("config.yaml")
    pipeline = generate_pipeline(settings)
    results, accuracy = evaluate_text_to_order(pipeline.order_proposal_service(), data_folder)

    print_results(results)
    logger.info(f"Overall accuracy: {accuracy}%")


if __name__ == "__main__":
    evaluate_model("./data/order_examples_test")
