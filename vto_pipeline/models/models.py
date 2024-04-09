from enum import Enum
from typing import Any

from flair.data import Span
from pydantic import BaseModel


class EntityType(str, Enum):
    PRODUCT = "Product"
    QUANTITY = "Quantity"
    UNIT = "Unit"
    OTHER = "Other"

    @staticmethod
    def from_str(label: str) -> "EntityType":
        return getattr(EntityType, label.upper())


class ChatgptRole(str, Enum):
    system = "system"
    user = "user"
    assistant = "assistant"


class ChatgptMessage(BaseModel):
    role: ChatgptRole
    content: str


class Entity(BaseModel):
    text: str
    category: EntityType
    confidence: float = 0

    @classmethod
    def from_span(span: Span) -> "Entity":
        try:
            category = EntityType.from_str(span.tag)
        except AttributeError:
            category = EntityType.OTHER
        return Entity(text=span.text, category=category, confidence=round(span.score, 2))


class Match(BaseModel):
    product_name: str
    product_category: str
    sku: str
    full_result: Any


class RecognizedProduct(BaseModel):
    quantity: str | int
    unit: str
    product_identifier: str


class Item(BaseModel):
    quantity: int
    unit: str
    sku: str
    product_name: str
    speech: str


class UnmatchedItem(Item):
    quantity: int = 0
    unit: str = "none"
    sku: str = 0
    product_name: str = "no match"
    speech: str


class OrderProposal(BaseModel):
    items: list[Item]
