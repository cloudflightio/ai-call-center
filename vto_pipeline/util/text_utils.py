import json
import os
import random
from typing import Tuple

from loguru import logger

from vto_pipeline.exceptions import EntityGroupingError
from vto_pipeline.models.entity_group import EntityGroup
from vto_pipeline.models.models import Entity, EntityType


def process_word_quantity(quantity: str) -> int:
    """Customers sometimes mention a quantity like 'drei mal' which we need to transform into an integer."""
    # TODO: Improve this method. This is only a quick n dirty solution
    try:
        return int(quantity)
    except ValueError:
        mappings = {
            "ein": 1,
            "zwei": 2,
            "drei": 3,
            "vier": 4,
            "fünf": 5,
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
        }
        try:
            return next(value for key, value in mappings.items() if key in quantity)
        except StopIteration:
            raise ValueError(f"Can't find integer for quantity string: '{quantity}'")


def load_example_order() -> Tuple[str, list[dict]]:
    data_folder = "./data/order_examples_test"
    i = random.randint(1, 50)
    file_path = os.path.join(data_folder, f"sentence_{i}.json")

    with open(file_path, "r") as f:
        order = json.load(f)
    return order["text"], order["products"]


def find_entity_groups(entities: list[Entity]) -> list[EntityGroup]:
    """From a given list of entities, return the groups containing entities belonging to the same item
    of the order. A group valid group can be mapped to a recognized product."""
    groups = []

    current_group = EntityGroup([entities[0]])
    for entity in entities[1:]:
        if (not current_group.sufficient) or (
            entity.category == EntityType.UNIT and EntityType.UNIT not in current_group.categories
        ):
            current_group.entities.append(entity)
        elif current_group.valid:
            groups.append(current_group)
            current_group = EntityGroup([entity])
        else:
            logger.debug(f"The given entities could not be grouped: {entities}.")
            raise EntityGroupingError

    # Add the group left open in the last iteration:
    if current_group.valid:
        groups.append(current_group)
    else:
        logger.debug(f"The given entities could not be grouped: {entities}.")
        raise EntityGroupingError

    return groups
