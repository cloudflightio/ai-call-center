import json
import os
import random

from utils import get_products, get_unit

QUANTITY_NR_OPTIONS = list(map(str, range(1, 10)))
QUANTITY_WORD_OPTIONS = ["einmal", "zweimal", "3 mal", "5 mal"]

PRODUCTS_DF = get_products()


def generate_product_entities() -> dict:
    """Get a coherent set of product, packaging and quantity from the dataset."""
    product = generate_product()

    product_entities = {
        "product": product["name"].values[0].strip(),
        "unit": get_unit(),
        "quantity": str(random.choice(QUANTITY_NR_OPTIONS)),
        "quantity_word": random.choice(QUANTITY_WORD_OPTIONS),
        "sku": int(product["sku"].values[0]),
    }
    return product_entities


def generate_product() -> str:
    """Sample a product from the dataset and clean the product name."""
    global PRODUCTS_DF

    product = PRODUCTS_DF.sample(n=1)
    PRODUCTS_DF = PRODUCTS_DF.drop(product.index)

    product_name = str(product["name"].values[0]).lower()
    product["name"] = clean_product_name(product_name)
    return product


def clean_product_name(product_name: str) -> str:
    """This should turn the product name into something a human would say."""
    # TODO: Implement some data cleaning here!
    return product_name


if __name__ == "__main__":
    N = 400  # Number of examples to generate

    products = []
    for i in range(N):
        p = generate_product_entities()
        products.append(p)

    json_data = json.dumps(products, indent=2)

    # Save the JSON string to a file
    mode = "test"
    filename = f"./data/product_entities_{mode}.json"
    if not os.path.exists(filename):
        with open(filename, "w") as json_file:
            json_file.write(json_data)
    else:
        raise FileExistsError(filename + " already exists.")
