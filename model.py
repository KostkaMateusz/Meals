from dataclasses import dataclass


@dataclass
class MealDataClass:
    __slots__ = ["name", "picture", "present_ingredients", "missing_ingredients", "carbs", "proteins", "calories"]
    name: str
    picture: str
    present_ingredients: list[str]
    missing_ingredients: list[str]
    carbs: float
    proteins: float
    calories: float


def make_list_of_meals(recipies: list) -> list[MealDataClass]:
    """Filtr response from spoonacular and create list of MealDataClass from needed information"""
    list_of_object = []

    for recipie_info in recipies["results"]:

        name = recipie_info["title"]
        picture = recipie_info["image"]
        present_ingredients = [ingridients["name"] for ingridients in recipie_info["usedIngredients"]]
        missing_ingredients = [missed_ingridients["name"] for missed_ingridients in recipie_info["missedIngredients"]]

        nutrients = {}
        for nutriotion in recipie_info["nutrition"]["nutrients"]:
            if nutriotion["name"] in ["Carbohydrates", "Protein", "Calories"]:
                nutrients.update({nutriotion["name"]: nutriotion["amount"]})

        recipe = MealDataClass(name, picture, present_ingredients, missing_ingredients, nutrients["Carbohydrates"], nutrients["Protein"], nutrients["Calories"])

        list_of_object.append(recipe)

    return list_of_object
