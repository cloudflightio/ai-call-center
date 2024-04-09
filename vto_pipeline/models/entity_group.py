from vto_pipeline.exceptions import CategoryNotFoundError, EntityGroupMappingError
from vto_pipeline.models.models import Entity, EntityType, RecognizedProduct


class EntityGroup:
    def __init__(self, entities: list[Entity]):
        """An entity group represents a single product that the customer wants to order. It is a group of entities
        that belong together. For example [2, bottles, wine, Hofer] can be a single group.

        A group can be sufficient or insufficient. A sufficient group contains enough information to reliably determine
        the correct order. The rule for a group to be sufficient is that it contains a Product and Quantity entity.

        A group is invalid if it contains more than one Entity of a certain category, and if it is not sufficient.
        Also, the unit - if it is present - must appear after the quantity
        """
        self.entities = entities

    def __eq__(self, other):
        return self.entities == other.entities

    def get_entity(self, entity: EntityType) -> Entity:
        """Remove only the quantity from the group. The leftover group is suitable for product matching."""
        try:
            return next(e for e in self.entities if e.category == entity)
        except StopIteration:
            raise CategoryNotFoundError

    def to_recognized_product(self) -> RecognizedProduct:
        if not self.valid:
            raise EntityGroupMappingError

        # A valid group does not necessarily have a unit so we need to handle this:
        try:
            unit = self.get_entity(EntityType.UNIT).text
        except CategoryNotFoundError:
            unit = "default"

        return RecognizedProduct(
            quantity=self.get_entity(EntityType.QUANTITY).text,
            unit=unit,
            product_identifier=self.get_entity(EntityType.PRODUCT).text,
        )

    @property
    def categories(self) -> list[EntityType]:
        return [e.category for e in self.entities]

    @property
    def sufficient(self) -> bool:
        """A group is complete when there is a quantity and product."""
        return EntityType.QUANTITY in self.categories and EntityType.PRODUCT in self.categories

    @property
    def valid(self) -> bool:
        """Every entity can appear at most once. The unit is optional but should be after the quantity if it appears."""
        return self.sufficient and self.unit_after_quantity and self.has_no_duplicates

    @property
    def has_no_duplicates(self) -> bool:
        unique_categories = [EntityType.PRODUCT, EntityType.UNIT, EntityType.QUANTITY]
        return all(not self.categories.count(c) > 1 for c in unique_categories)

    @property
    def unit_after_quantity(self) -> bool:
        if EntityType.UNIT not in self.categories:
            return True

        if self.entities[0].category == EntityType.UNIT:
            return False

        for i, e in enumerate(self.entities):
            if e.category == EntityType.QUANTITY:
                return EntityType.UNIT in EntityGroup(self.entities[i + 1 :]).categories

        return False
