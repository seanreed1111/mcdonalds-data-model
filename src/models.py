from enum import StrEnum

from pydantic import BaseModel, Field


class Size(StrEnum):
    SNACK = "snack"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class Category(BaseModel):
    category_id: str
    name: str


class Modifier(BaseModel):
    modifier_id: str
    name: str
    restrictions: list["Category"] = Field(default_factory=list)


class Item(BaseModel):
    item_id: str
    name: str
    category_name: str
    size: Size = Field(default=Size.MEDIUM)
    quantity: int = Field(default=1, ge=1)
    modifiers: list[Modifier] = Field(default_factory=list)


class Combo(BaseModel):
    combo_id: str
    items: list[Item]
    quantity: int = Field(default=1, ge=1)


class Menu(BaseModel):
    name: str
    allowed_categories: list[Category]
