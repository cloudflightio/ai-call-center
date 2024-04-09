import json
import os
import random

from loguru import logger

INTRO_TEMPLATES = ["Hallo, hier spricht {name} von {org}.", "Hier spricht {name}.", "Servus, hier {name}. "]

SENTENCE_TEMPLATES = [
    "Ich möchte von {product_1} {quantity_1} {unit_1} und von {product_2} {quantity_2} {unit_2} in meiner Bestellung.",
    "Könnten Sie mir bitte {quantity_1} {unit_1} {product_1} und von {product_2} {quantity_2} {unit_2} zusenden?",
    "Bitte fügen Sie zu meiner Bestellung {quantity_1} {unit_1} {product_1} und {quantity_word_2} {product_2} hinzu.",
    "{product_1}, {quantity_word_1} und {quantity_2} {unit_2} {product_2} bitte in meiner Bestellung berücksichtigen.",
    "Gibt es Rabatt für die Bestellung von {quantity_1} {unit_1} {product_1} und {quantity_2} {unit_2} {product_2}?",
    """Ich interessiere mich für {product_1} {quantity_1} {unit_1} und {quantity_word_2} {product_2} und würde gerne
        eine Bestellung aufgeben.""",
    "Welche Zahlungsmethoden akzeptieren Sie für {quantity_1} {unit_1} {product_1} und {quantity_word_2} {product_2}?",
    "{product_1} und {product_2} jeweils in {quantity_1} {unit_1} bitte zu meiner Bestellung hinzufügen.",
    "Können Sie mir ein Angebot für {quantity_1} {unit_1} {product_1}, {quantity_2} {unit_2} {product_2} zusenden?",
    "Bestätigen Sie den Empfang mein Bestellung für {quantity_1} {unit_1} {product_1}, {quantity_word_2} {product_2}.",
]


def generate_order_example(p_1: dict, p_2: dict):
    sentence = random.choice(SENTENCE_TEMPLATES)
    sentence = sentence.format(
        product_1=p_1["product"],
        unit_1=p_1["unit"],
        quantity_1=p_1["quantity"],
        quantity_word_1=p_1["quantity_word"],
        product_2=p_2["product"],
        unit_2=p_2["unit"],
        quantity_2=p_2["quantity"],
        quantity_word_2=p_2["quantity_word"],
    )
    return sentence


TEST = False  # Hint: CHANGE THIS TO GENERATE A TRAIN OR TEST DATASET

if __name__ == "__main__":
    mode = "test" if TEST else "train"

    # Read product examples to put into the sentences:
    with open(f"./data/product_entities_{mode}.json", "r") as json_file:
        product_entities = json.load(json_file)

    data_directory = f"./data/order_examples_{mode}"
    os.makedirs(data_directory, exist_ok=True)

    for i in range(int(len(product_entities) / 2)):
        p_1, p_2 = random.sample(product_entities, 2)
        order = generate_order_example(p_1, p_2)

        file_path = os.path.join(data_directory, f"sentence_{i}.json")

        data = {"text": order, "products": [p_1, p_2]}
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

    logger.info("Dataset generated succesfully")
