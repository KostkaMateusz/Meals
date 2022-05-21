from dataclasses import dataclass


@dataclass
class Recipe:
    __slots__ = ["name", "picture", "present_ingredients", "missing_ingredients", "carbs", "proteins", "calories"]
    name: str
    picture: str
    present_ingredients: list[str]
    missing_ingredients: list[str]
    carbs: float
    proteins: float
    calories: float
