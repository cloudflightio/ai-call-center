import pytest

from vto_pipeline.models.models import EntityType


@pytest.mark.unit
@pytest.mark.parametrize(
    "type, expected",
    [
        ("product", EntityType.PRODUCT),
        ("unit", EntityType.UNIT),
        ("quantity", EntityType.QUANTITY),
        ("other", EntityType.OTHER),
    ],
)
def test_entitytype_from_str(type: str, expected: EntityType):
    order_entity = EntityType.from_str(type)
    assert order_entity == expected


@pytest.mark.unit
def test_entitytype_from_str_invalid():
    with pytest.raises(AttributeError):
        EntityType.from_str("invalid")
