import json
import os
from typing import Tuple

from loguru import logger

from vto_pipeline.exceptions import EntityGroupingError, NoProductsRecognizedError
from vto_pipeline.models.models import Item, OrderProposal
from vto_pipeline.services.order_generation import OrderProposalService


def evaluate_text_to_order(
    order_generator: OrderProposalService, data_folder: str
) -> Tuple[list[dict], float]:
    results = []
    n = 0  # number of products matched
    overall_accuracy = 0
    i = 0
    while True:
        file_path = os.path.join(data_folder, f"sentence_{i}.json")
        logger.info(f"Analysing sentence {i}...", end="\r")
        i += 1

        try:
            with open(file_path, "r") as f:
                order = json.load(f)
        except FileNotFoundError:
            break

        text = order["text"]
        true_products = order["products"]

        try:
            order_proposal = order_generator.from_text(text)
        except EntityGroupingError:
            continue
        except NoProductsRecognizedError:
            # We need to consider this as a valid result for the evaluation
            order_proposal = OrderProposal(items=[])

        result = {
            "text": text,
            "true_products": true_products,
            "predicted_products": order_proposal.items,
            "accuracy": get_accuracy(true_products, order_proposal.items),
        }

        n, overall_accuracy = update_overall_accuracy(result, n, overall_accuracy)
        results.append(result)
    return results, overall_accuracy


def update_overall_accuracy(result: dict, n: int, overall_accuracy: float):
    """Update the overall accuracy calculated over n items with the new items (and their accuracy) in the result
    dict."""
    a_new = result["accuracy"]
    n_new = len(result["true_products"])

    new_overall_accuracy = (overall_accuracy * n + a_new * n_new) / (n + n_new)
    return n + n_new, new_overall_accuracy


def get_accuracy(true_products: list[dict], predicted_items: list[Item]):
    """Check the percentage of the products that match the items."""
    sku_predicted = [i.sku for i in predicted_items]
    sku_true = [p["sku"] for p in true_products]

    correct = len(set(sku_true) & set(sku_predicted))
    wrong = len(sku_true) - correct

    percentage_correct = correct / (correct + wrong)
    return percentage_correct


def print_results(results: list[dict]):
    for r in results:
        logger.info(f"Order accuracy {r['accuracy']}:")
        for p in r["true_products"]:
            logger.info(f"Order: {p['product']}")
        if len(r["predicted_products"]) == 0:
            logger.info("No products recognized.")
        else:
            for i in r["predicted_products"]:
                logger.info(f"Matches: {i.product_name}")
        logger.info("\n")
