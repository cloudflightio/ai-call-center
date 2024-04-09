import json
import random

import pandas as pd


def get_unit():
    """Extract the packaging method as text"""
    # TODO: Just pick random value
    with open("./data/packaging_methods.json", "r") as file:
        packaging_methods = json.load(file)
    return random.choice(packaging_methods)


def get_products() -> pd.DataFrame:
    return pd.read_json("./data/products.json")
