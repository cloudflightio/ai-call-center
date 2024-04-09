import pytest

from vto_pipeline.exceptions import CategoryNotFoundError, EntityGroupMappingError
from vto_pipeline.models.entity_group import EntityGroup
from vto_pipeline.models.models import Entity, EntityType, RecognizedProduct


@pytest.mark.unit
def test_entity_group_equals():
    e_1 = Entity(text="Test", category=EntityType.PRODUCT)
    g_1 = EntityGroup([e_1])

    # should be the same
    e_2 = Entity(text="Test", category=EntityType.PRODUCT)
    g_2 = EntityGroup([e_2])

    # different text
    e_3 = Entity(text="Different", category=EntityType.PRODUCT)
    g_3 = EntityGroup([e_3])

    # different category
    e_4 = Entity(text="Test", category=EntityType.QUANTITY)
    g_4 = EntityGroup([e_4])

    # different confidence
    e_5 = Entity(text="Test", category=EntityType.PRODUCT, confidence=1)
    g_5 = EntityGroup([e_5])

    assert g_1 == g_2
    assert g_1 != g_3
    assert g_1 != g_4
    assert g_1 != g_5


@pytest.mark.unit
def test_entity_group_get_entity():
    e = Entity(text="Test", category=EntityType.PRODUCT)
    g = EntityGroup([e])

    # get category from group
    assert g.get_entity(EntityType.PRODUCT) == e

    # get category not in group
    with pytest.raises(CategoryNotFoundError):
        g.get_entity(EntityType.OTHER)


@pytest.mark.unit
def test_entity_group_to_recognized_product():
    p = Entity(text="Product", category=EntityType.PRODUCT)
    u = Entity(text="Unit", category=EntityType.UNIT)
    q = Entity(text="Quantity", category=EntityType.QUANTITY)

    g = EntityGroup([p, q, u])
    result = g.to_recognized_product()

    expected = RecognizedProduct(quantity="Quantity", unit="Unit", product_identifier="Product")
    assert result == expected


@pytest.mark.unit
def test_entity_group_to_recognized_product_invalid_group():
    p = Entity(text="Product", category=EntityType.PRODUCT)
    u = Entity(text="Unit", category=EntityType.UNIT)
    q = Entity(text="Quantity", category=EntityType.QUANTITY)

    g = EntityGroup([p, u, q])
    with pytest.raises(EntityGroupMappingError):
        g.to_recognized_product()


@pytest.mark.unit
def test_entity_group_to_recognized_product_no_unit():
    p = Entity(text="Product", category=EntityType.PRODUCT)
    q = Entity(text="Quantity", category=EntityType.QUANTITY)

    g = EntityGroup([p, q])
    result = g.to_recognized_product()

    expected = RecognizedProduct(quantity="Quantity", unit="default", product_identifier="Product")
    assert result == expected


@pytest.mark.unit
def test_entity_group_append_entity():
    e = Entity(text="Test", category=EntityType.PRODUCT)
    g = EntityGroup([e])

    assert g.entities == [e]

    g.entities.append(e)
    assert g.entities == [e, e]


@pytest.mark.unit
def test_entity_group_categories():
    e0 = Entity(text="Product", category=EntityType.PRODUCT)
    e1 = Entity(text="Unit", category=EntityType.UNIT)
    e2 = Entity(text="Other", category=EntityType.OTHER)
    g = EntityGroup([e0, e1, e2])
    assert g.categories == [EntityType.PRODUCT, EntityType.UNIT, EntityType.OTHER]


@pytest.mark.unit
def test_entity_group_categories_duplicates():
    e0 = Entity(text="Test", category=EntityType.PRODUCT)
    e1 = Entity(text="Test", category=EntityType.PRODUCT)
    e2 = Entity(text="Test", category=EntityType.OTHER)
    g = EntityGroup([e0, e1, e2])
    assert g.categories == [EntityType.PRODUCT, EntityType.PRODUCT, EntityType.OTHER]


@pytest.mark.unit
def test_entity_group_sufficient():
    p = Entity(text="Test", category=EntityType.PRODUCT)
    q = Entity(text="Test", category=EntityType.QUANTITY)

    g = EntityGroup([p])
    assert not g.sufficient

    g = EntityGroup([q])
    assert not g.sufficient

    g = EntityGroup([p, q])
    assert g.sufficient


@pytest.mark.unit
def test_entity_group_valid():
    p = Entity(text="Test", category=EntityType.PRODUCT)
    q = Entity(text="Test", category=EntityType.QUANTITY)
    u = Entity(text="Test", category=EntityType.UNIT)
    o = Entity(text="Test", category=EntityType.OTHER)

    g0 = EntityGroup([p, q, u])
    assert g0.valid

    # product must be there
    g1 = EntityGroup([u, q])
    assert not g1.valid

    # quantity must be there
    g2 = EntityGroup([p, u])
    assert not g2.valid

    # no duplicates allowed
    g3 = EntityGroup([p, p, q])
    assert not g3.valid

    # not unit before quantity
    g4 = EntityGroup([u, p, q])
    assert not g4.valid

    # other is allowed at any point:
    g5 = EntityGroup([o, p, o, q, o, u, o])
    assert g5.valid


@pytest.mark.unit
def test_entity_group_has_no_duplicates():
    p = Entity(text="Test", category=EntityType.PRODUCT)

    g = EntityGroup([p])
    assert g.has_no_duplicates

    g = EntityGroup([p, p])
    assert not g.has_no_duplicates

    # other is allowed multiple times
    o = Entity(text="Test", category=EntityType.OTHER)
    g = EntityGroup([o, o])
    assert g.has_no_duplicates


@pytest.mark.unit
def test_entity_group_unit_after_quantity():
    p = Entity(text="Test", category=EntityType.PRODUCT)
    q = Entity(text="Test", category=EntityType.QUANTITY)
    u = Entity(text="Test", category=EntityType.UNIT)

    g2 = EntityGroup([p])
    assert g2.unit_after_quantity

    g0 = EntityGroup([q, u])
    assert g0.unit_after_quantity

    g1 = EntityGroup([u, q])
    assert not g1.unit_after_quantity

    g3 = EntityGroup([p, u])
    assert not g3.unit_after_quantity
